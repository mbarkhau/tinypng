#!/usr/bin/env python
from __future__ import unicode_literals

import os
import io

from os.path import abspath, isfile, join, expanduser
from base64 import standard_b64encode

import requests
from requests.exceptions import HTTPError

from tinypng.common import __version__, TINY_URL
from tinypng.common import TinyPNGException

CONTENTTYPE_JSON = "application/json; charset=utf-8"


def read_keyfile(filepath):
    with io.open(filepath, 'r', encoding='utf-8') as kf:
        return set([k.strip() for k in kf.readlines() if k.strip()])


def find_keys(args):
    """Get keys specified in arguments

    returns list of keys or None
    """
    key = args['--key']
    if key:
        return [key]

    keyfile = args['--apikeys']
    if keyfile:
        return read_keyfile(keyfile)

    envkey = os.environ.get('TINYPNG_API_KEY', None)
    if envkey:
        return [envkey]

    local_keys = join(abspath("."), "tinypng.keys")

    if isfile(local_keys):
        return read_keyfile(local_keys)

    home_keys = join(expanduser("~/.tinypng.keys"))
    if isfile(home_keys):
        return read_keyfile(home_keys)

    return []


def _shrink_info(in_data, api_key):
    if api_key is None:
        raise TypeError(
            "Missing required argument 'api_key' for tinypng.shrink_*()."
            "You may get a key from info@tinypng.org."
        )

    raw_key = ("api:" + api_key).encode('ascii')
    enc_key = standard_b64encode(raw_key).decode('ascii')
    try:
        resp = requests.post(TINY_URL, data=in_data, headers={
            "Authorization": "Basic {0}".format(enc_key),
            "X-PY-TinyPng": __version__
        })

        if resp.status_code != 201:
            raise HTTPError(response=resp)

        info = resp.json()
        info['compression_count'] = resp.headers['Compression-Count']
        info['url'] = resp.headers['Location']
        return info
    except HTTPError as err:
        if err.response.headers['content-type'] != CONTENTTYPE_JSON:
            raise
        raise TinyPNGException(
            info=err.response.json(),
            status_code=err.response.status_code
        )


def get_shrink_data_info(in_data, api_key=None):
    """Shrink binary data of a png

    returns api_info
    """
    if api_key:
        return _shrink_info(in_data, api_key)

    api_keys = find_keys()
    for key in api_keys:
        try:
            return _shrink_info(in_data, key)
        except ValueError:
            pass

    raise ValueError('No valid api key found')


def get_shrunk_data(shrink_info):
    """Read shrunk file from tinypng.org api."""
    out_url = shrink_info['output']['url']
    try:
        return requests.get(out_url).content
    except HTTPError as err:
        if err.code != 404:
            raise

        exc = ValueError("Unable to read png file \"{0}\"".format(out_url))
        exc.__cause__ = err
        raise exc


def shrink_data(in_data, api_key=None):
    """Shrink binary data of a png

    returns (api_info, shrunk_data)
    """
    info = get_shrink_data_info(in_data, api_key)
    return info, get_shrunk_data(info)


def get_shrink_file_info(in_filepath, api_key=None, out_filepath=None):
    with io.open(in_filepath, 'rb') as f:
        info = get_shrink_data_info(f.read(), api_key)

    if out_filepath is None:
        out_filepath = in_filepath
        prefix, ext = out_filepath.rsplit(".", 1)
        out_filepath = prefix + ".tiny." + ext

    info['output']['filepath'] = abspath(out_filepath)
    return info


def write_shrunk_file(info):
    out_filepath = info['output']['filepath']
    with io.open(out_filepath, 'wb') as f:
        f.write(get_shrunk_data(info))


def shrink_file(in_filepath, api_key=None, out_filepath=None):
    """Shrink png file and write it back to a new file

    The default file path replaces ".png" with ".tiny.png".
    returns api_info (including info['ouput']['filepath'])
    """
    info = get_shrink_file_info(in_filepath, api_key, out_filepath)
    write_shrunk_file(info)
    return info
