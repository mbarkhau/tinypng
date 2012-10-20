#!/usr/bin/env python
"""TinyPNG API

Python module and command line tool for api.tinypng.org

Important: You require an API key which you may obtain from
info@tinypng.org (as of October 2012).

Besides specifying keys via command line arguments you can
    1. Set the environment variable TINYPNG_API_KEY
    2. Create a .tinypng.keys file in your home directory
    3. Create a tinypng.keys file in the current directory

Keyfiles must have one key per line. Invalid keys should
be removed as they slow down requests.

Usage:
    tinypng.py <png_files>...
    tinypng.py <png_files>...
    tinypng.py --key=<key> <png_files>...
    tinypng.py --apikeys=<keyfile> <png_files>...
    tinypng.py -h | --help
    tinypng.py --version

Options:
    --key=<key>                 API Key
    --apikeys=<keyfile>         File with one key per line
    --extension=<extension>     Suffix of new images [default: .tiny.png]
    -h --help                   Show this screen
    --version                   Show version.
"""
from __future__ import print_function

import os
import sys
import json
from os.path import abspath, isfile, join, expanduser
from base64 import standard_b64encode

try:
    from urllib2 import Request, HTTPError, urlopen
except ImportError:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError


TINY_URL = "http://api.tinypng.org/api/shrink"
_invalid_keys = set()


def tinypng_info(in_data, api_key):
    if api_key is None:
        msg = "tinypng() requirs the 'api_key' argument. "
        msg += "You may get a key from info@tinypng.org."
        raise TypeError(msg)

    raw_key = ("api:" + api_key).encode('ascii')
    enc_key = standard_b64encode(raw_key).decode('ascii')
    request = Request(TINY_URL, in_data)
    request.add_header("Authorization", "Basic %s" % enc_key)

    try:
        result = urlopen(request)
        return json.loads(result.read().decode('utf8'))
    except HTTPError as err:
        if err.code == 403:
            raise ValueError("Invalid argument api key")

        print("TinyPNG Error: ", err.code)
        print(err.read())
        return


def tinypng_data(in_data, api_key):
    info = tinypng_info(in_data, api_key)
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


def tinypng_file(in_filepath, out_filepath=None, api_key=None):
    if out_filepath is None:
        out_filepath = in_filepath
        if out_filepath.endswith(".png"):
            out_filepath = out_filepath[:-4]
        out_filepath += ".tiny.png"

    in_data = open(in_filepath, 'rb').read()

    out_info, out_data = tinypng_data(in_data, api_key)
    out_info['output']['filepath'] = abspath(out_filepath)

    with open(out_filepath, 'wb') as f:
        f.write(out_data)

    return out_info


def findkeys(opts=None, args=None):
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


def main(argv=sys.argv):
    if argv is None:
        argv = sys.argv

    from docopt import docopt

    opts, args = docopt(__doc__, argv=argv[1:], version='TinyPNG API 1.0')
    keys = findkeys(opts, args)

    if keys is None:
        print("Error: Could not find API key (see help).")
        return 1

    print(keys)


if __name__ == "__main__":
    sys.exit(main())
