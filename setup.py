#!/usr/bin/env python

from distutils.core import setup

setup(
    name='manot',
    version='0.1.0',
    description='the manot package',
    author='manot',
    author_email='info@manot.ai',
    url='https://www.manot.ai',
    packages=['manot'],
    package_dir={'manot': 'src/manot'},
)