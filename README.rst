TinyPNG API
-----------

Python module and command line tool for `tinypng.com`_

Shrink PNG files. Advanced lossy compression for PNG images that
preserves full alpha transparency. Now also works with JPEG files.

Note: This project is not affiliated with `tinypng.com`_ or `Voormedia
B.V.`_

Important: You require an API key which you may obtain from
`tinypng.com/developers`_.

Besides specifying keys via command line arguments you can:

1. Set the environment variable TINYPNG\_API\_KEY
2. Create a .tinypng.keys file in your home directory
3. Create a tinypng.keys file in the current directory

Programatic api
~~~~~~~~~~~~~~~

::

    from tinypng import shrink_file

    # implicitly writes to "your_file.tiny.png"
    shrink_info = shrink_file("your_file.png", api_key='your_key_here')

    shrink_info = shrink_file(
        "your_input_file.png",
        api_key='your_key_here',
        out_filepath="your_output_file.png"
    )

    shrink_info == {
        "output": {
            "type": "image/png",
            "filepath": "/path/your_input_file.png",
            "size": 36988,
            "ratio": 0.8279,
            "url": "https://api.tinypng.com/output/abcdefg123456.jpg"
        },
        "url": "https://api.tinypng.com/output/abcdefg123456.jpg",
        "compression_count": "123",
        "input": {
            "type": "image/png",
            "size": 44679
        }
    }

.. _tinypng.com: https://tinypng.com
.. _Voormedia B.V.: http://voormedia.com/
.. _tinypng.com/developers: https://tinypng.com/developers
