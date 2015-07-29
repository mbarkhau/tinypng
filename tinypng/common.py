__version__ = "2.2.0"

import sys

from __future__ import print_function
from __future__ import unicode_literals

PY2 = sys.version < "3"
if PY2:
    input = raw_input

import io

def open(filename, mode='r', **kwargs):
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'utf-8'
    if 'b' in mode:
        kwargs['encoding'] = None
    return io.open(filename, mode, **kwargs)

TINY_URL = "https://api.tinypng.com/shrink"

class TinyPNGException(Exception):

    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info')
        self.error = self.info['error']
        self.message = self.info['message']
        self.status_code = kwargs.pop('status_code')

API_KEY_ERRORS = ('Unauthorized',)
RATE_LIMIT_ERRORS = ('TooManyRequests',)
MISC_ERRORS = (
    'BadSignature', 'InputMissing', 'DecodeError', 'InternalServerError'
)

