from __future__ import print_function
from __future__ import unicode_literals

__version__ = '3.0.0'


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

