from __future__ import unicode_literals

import os
import io

from setuptools import setup
from tinypng.common import __version__


def read(fname):
    fpath = os.path.join(os.path.dirname(__file__), fname)
    with io.open(fpath, 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='tinypng',
    version=__version__,
    description='Access api.tinypng.org from the shell and python scripts',
    long_description=read('README.rst'),
    author='Manuel Barkhau',
    author_email='mbarkhau@gmail.com',
    url='https://github.com/mbarkhau/tinypng/',
    license="BSD License",
    packages=['tinypng'],
    install_requires=['docopt>=0.6', 'requests>=2.0'],
    extras_require={'dev': ["wheel", "pytest"]},
    entry_points="""
        [console_scripts]
        tinypng=tinypng.cmd:main
    """,
    keywords="png image compression tinypng shrink jpeg jpg",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        'Topic :: Utilities',
    ],

)
