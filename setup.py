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
    description='ModelGenie',
    author='Cindy Cao',
    author_email='cindy@datanarra.com',
    url='http://github.com/cindyc/datanarra/modelgenie',
    install_requires=[requirements, dev_requirements],
    packages=['modelgenie', 'persistence', 'api'],
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
