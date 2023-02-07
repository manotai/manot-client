#!/usr/bin/env python

from distutils.core import setup

setup(
    name='manot',
    version='0.6.1',
    description='The manot SDK is a wrapper on top of our API to make it easier to work with our model performance monitoring system. Using our SDK you can quickly set up your project by defining a few key parameters, including the paths to your data, classes and model. Once the project is set up you will be able to use the insight method to extract outliers that manot has detected on the new unstructured data that the performance of the model is evaluated on.',
    author='manot',
    author_email='engineering@manot.ai',
    url='https://www.manot.ai',
    packages=['manot'],
    package_dir={'manot': 'src/manot'},
)
