from setuptools import setup
from os.path import join, dirname


def read(fname):
    return open(join(dirname(__file__), fname)).read()


setup(
    name='tinypng',
    version='1.0',
    description='Access api.tinypng.org from the shell and python scripts',
    long_description=read('README'),
    author='Manuel Barkhau',
    author_email='mbarkhau@gmail.com',
    url='http://bitbucket.org/mbarkhau/tinypng/',
    license="MIT",
    packages=['tinypng'],
    requires=['docopt'],
    entry_points={'console_scripts': ["tinypng = tinypng:main"]},
    keywords="png image compression",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],

)
