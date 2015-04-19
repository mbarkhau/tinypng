
__version__ = "2.1.4"

TINY_URL = "https://api.tinypng.com/shrink"

class TinyPNGException(Exception):

    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info')
        self.error = self.info['error']
        self.message = self.info['message']
        self.status_code = kwargs.pop('status_code')

