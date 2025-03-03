#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='domaintools',
    version='1.0.1',
    description='Domain parsing with python',
    author='DevHub',
    url='http://github.com/devhub/domaintools',
    packages=find_packages(),
    install_requires=[
        'tldextract == 2.2.3',
    ]
)
