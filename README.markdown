TinyPNG API
-----------

Python module and command line tool for [tinypng.org][1]

Shrink PNG files. Advanced lossy compression for PNG images
that preserves full alpha transparency.

Note: This project is not affiliated with [tinypng.org][1] or [Voormedia B.V.][2]

Important: You require an API key which you may obtain from
[info@tinypng.org][3] (as of October 2012).


Besides specifying keys via command line arguments you can:

1. Set the environment variable TINYPNG_API_KEY
2. Create a .tinypng.keys file in your home directory
3. Create a tinypng.keys file in the current directory

Keyfiles must have one key per line. Invalid keys should
be removed as they slow down requests.


[1]: http://tinypng.org
[2]: http://voormedia.com/
[3]: mailto:info@tinypng.org