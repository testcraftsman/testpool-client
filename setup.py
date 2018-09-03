#!/usr/bin/python
import logging
import os
import pkgutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

AUTHOR = "Mark Hamilton"
AUTHOR_EMAIL = "mark.lee.hamilton@gmail.com"

CMD = "cat VERSION"
VERSION = subprocess.check_output(CMD, shell=True).replace("\n", "")

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

fpath = os.path.join(os.path.dirname(__file__), 'requirements.txt')

with open(fpath) as hdl:
    REQUIREMENTS = hdl.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup_args = {
    "name": 'testpool-client',
    "version": VERSION,
    "packages": find_packages(),
    "include_package_data": True,
    "license": 'GPLv3',
    "description": 'Client to Testpool.',
    "long_description": README,
    "url": 'https://github.com/testbed/testpool-client.git',
    "maintainer": AUTHOR,
    "maintainer_email": AUTHOR_EMAIL,
    "author": AUTHOR,
    "author_email": AUTHOR_EMAIL,
    "install_requires": REQUIREMENTS,
    "classifiers": [
        'Development Status :: 1 - Pre-Alpha',
        'Programming Language :: Python :: 2.7',
    ],
}
setup(**setup_args)
