#!/usr/bin/env python
"""TinyPNG API

Python module and command line tool for api.tinypng.com

Shrink PNG files. Advanced lossy compression for PNG images
that preserves full alpha transparency.

Note: This project is not affiliated with tinypng.com or Voormedia B.V.

Important: You require an API key which you can obtain from
    https://tinypng.com/developers.

Usage:
    tinypng <png_files>...
            [--key=<key>] [--apikeys=<keyfile>]
            [--replace] [--quiet] [--verbose]
    tinypng -h | --help
    tinypng --version

Options:
    --key=<key>                 API Key
    --apikeys=<keyfile>         File with one key per line
    -h --help                   Show this screen
    -q --quiet                  Don't display api and file compression info
    --version                   Show version.
"""
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import sys

if sys.version < "3":
    input = raw_input
else:
    input = input

from docopt import docopt

from tinypng.api import get_shrink_file_info, write_shrunk_file, find_keys
from tinypng.common import TinyPNGException
from tinypng.common import __version__

from tinypng.common import API_KEY_ERRORS, RATE_LIMIT_ERRORS, MISC_ERRORS


def main(argv=sys.argv[1:]):
    def pout(s):
        if args['--quiet']:
            return
        sys.stdout.write(s)
        sys.stdout.flush()

    version = "TinyPNG API " + __version__
    args = docopt(__doc__, argv=argv, version=version)
    keys = find_keys(args)

    if not keys:
        print(
            "tinypng: No API key found\n"
            "  You can obtain a key from https://tinypng.com/developers"
        )
        key = input("  Enter API key: ").strip()
        if not key:
            return 1

        keypath = os.path.join(os.path.expanduser("~"), ".tinypng.keys")

        with io.open(keypath, 'w', encoding='utf-8') as f:
            f.write(key +  "\n")

        pout("tinypng: Created keyfile at {0}\n".format(keypath))

        keys = set([key])

    for fpath in args['<png_files>']:
        outpath = fpath if args['--replace'] else None
        cur_keys = keys.copy()
        for key in cur_keys:
            try:
                pout("tinypng: Shrinking '{0}' .. ".format(fpath))
                info = get_shrink_file_info(
                    fpath, api_key=key, out_filepath=outpath
                )
                pout("ok.\n")
                out_info = info['output']
                in_info = info['input']
                pout("tinypng: Saved {0:02d}% ({1} byte -> {2} byte)\n".format(
                    int(100 - (out_info['ratio'] * 100)),
                    in_info['size'], out_info['size'],
                ))
                pout("tinypng: {0} compressions this month\n".format(
                    info['compression_count'],
                ))

                if out_info['ratio'] < 1:
                    pout("tinypng: Writing to '{0}' .. ".format(
                        out_info['filepath']
                    ))
                    write_shrunk_file(info)
                    pout("done.\n")

                break
            except TinyPNGException as e:
                pout("fail!\n")
                pout("\ntinypng: {0}\t\t{1}\n".format(e.error, e.message))

                if e.error in MISC_ERRORS:
                    break # try other files which may be valid

                if e.error in API_KEY_ERRORS:
                    pout("tinypng: Invalid API key \"{0}\"\n".format(key))

                if e.error in RATE_LIMIT_ERRORS:
                    msg_fmt = "tinypng: API Limit exceeded for \"{0}\"\n"
                    pout(msg_fmt.format(key))

                if e.error in API_KEY_ERRORS + RATE_LIMIT_ERRORS:
                    keys.remove(key)
                    continue # try again if other keys are available

            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
