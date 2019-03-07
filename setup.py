"""
PySoundIo

A robust, cross-platform solution for real-time audio.
"""
import re
import sys 
import os
import platform
from setuptools import setup, Extension

def is_win():
    return sys.platform.startswith("win")

def is_os_64bit():
    return platform.machine().endswith("64")


vstr = open('pysoundio/__init__.py', 'r').read()
regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
version = re.search(regex, vstr, re.M)


if is_win():
    if is_os_64bit():
        LIBRARY_DIRS = [os.path.abspath('./pysoundio/libs/win/64')]
    else:
        LIBRARY_DIRS = [os.path.abspath('./pysoundio/libs/win/32')]

else:
    LIBRARY_DIRS = ['/usr/local/lib']

soundio = Extension('_soundiox',
                    sources=['pysoundio/_soundiox.c'],
                    include_dirs=['./pysoundio', '/usr/local/include'],
                    library_dirs=LIBRARY_DIRS,
                    libraries=['soundio'])

setup(
    name='pysoundio',
    version=version.group(1),
    description='Python wrapper for libsoundio',
    long_description='A robust, cross-platform solution for real-time audio',
    license='MIT',
    author='Joe Todd',
    author_email='joextodd@gmail.com',
    url='http://pysoundio.readthedocs.io/en/latest/',
    download_url='https://github.com/joextodd/pysoundio/archive/' + version.group(1) + '.tar.gz',
    include_package_data=True,
    packages=['pysoundio'],
    ext_modules=[soundio],
    test_suite='tests',
    zip_safe=False,
    keywords=('audio', 'sound', 'stream'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License'
    ],
)
