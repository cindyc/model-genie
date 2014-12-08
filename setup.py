#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup

from modelgenie import __version__


REQUIREMENTS_FILE = 'requirements.txt'
DEV_REQUIREMENTS_FILE = 'dev-requirements.txt'


dev_requirements = open(
        os.path.join(os.path.dirname(__file__), DEV_REQUIREMENTS_FILE)).read().split()
requirements = open(
        os.path.join(os.path.dirname(__file__), REQUIREMENTS_FILE)).read().split()

setup(
    name='modelgenie', 
    license='',
    version=__version__,
    description='Turn Unstructured Data to Structured Data',
    author='Cindy Cao',
    author_email='cindy@candidnarrative.com',
    url='http://github.com/cindyc/model-genie',
    install_requires=requirements,
    packages=['modelgenie',],
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
