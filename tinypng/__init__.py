#!/usr/bin/env python
from __future__ import print_function
__version__ = "1.0.5"

import os
import json
from os.path import abspath, isfile, join, expanduser
from base64 import standard_b64encode

try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import Request, HTTPError, urlopen


TINY_URL = "http://api.tinypng.org/api/shrink"
_invalid_keys = set()


def find_keys(opts=None, args=None):
    """Get keys specified in arguments

    returns list of keys or None
    """
    def readkeys(filepath):
        with open(filepath) as kf:
            return [k.strip() for k in kf.readlines()]

    if opts.key:
        return [opts.key]

    if opts.apikeys:
        return readkeys(opts.apikeys)

    envkey = os.environ.get('TINYPNG_API_KEY', None)
    if envkey:
        return [envkey]

    local_keys = join(abspath("."), "tinypng.keys")
    home_keys = join(expanduser("~/.tinypng.keys"))

    if isfile(local_keys):
        return readkeys(local_keys)
    if isfile(home_keys):
        return readkeys(local_keys)

    return None


def shrink(in_data, api_key):
    if api_key is None:
        msg = "Missing required argument 'api_key' for tinypng.shrink_*()."
        msg += "You may get a key from info@tinypng.org."
        raise TypeError(msg)

    if api_key in _invalid_keys:
        raise ValueError("Invalid argument api key")

    raw_key = ("api:" + api_key).encode('ascii')
    enc_key = standard_b64encode(raw_key).decode('ascii')
    request = Request(TINY_URL, in_data)
    request.add_header("Authorization", "Basic %s" % enc_key)

    try:
        result = urlopen(request)
        return json.loads(result.read().decode('utf8'))
    except HTTPError as err:
        if err.code == 403:
            _invalid_keys.add(api_key)
            raise ValueError("Invalid argument api key")

        print("TinyPNG Error: ", err.code)
        print(err.read())
        return


def shrink_data(in_data, api_key):
    info = shrink(in_data, api_key)
    out_url = info['output']['url']
    try:
        return info, urlopen(out_url).read()
    except HTTPError as err:
        if err.code != 404:
            raise

        msg = 'Unable to read png file "%s"' % out_url
        exc = ValueError(msg)
        exc.__cause__ = err
        raise exc


def shrink_file(in_filepath, out_filepath=None, api_key=None):
    if out_filepath is None:
        out_filepath = in_filepath
        if out_filepath.endswith(".png"):
            out_filepath = out_filepath[:-4]
        out_filepath += ".tiny.png"

    in_data = open(in_filepath, 'rb').read()

    out_info, out_data = shrink_data(in_data, api_key)
    out_info['output']['filepath'] = abspath(out_filepath)
    with open(out_filepath, 'wb') as f:
        f.write(out_data)

    return out_info
