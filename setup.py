#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup

from modelgenie import __version__

requirements = [
        'flask>=0.10.1',
        'flask-restful',
        'flask-cors',
        'pymongo==3.0.1',
        'schematics',
        'six',
]

dev_requirements = [
        'pytest==2.7.2',
]

setup(
    name='modelgenie',
    license='',
    version=__version__,
    description='ModelGenie',
    author='Cindy Cao',
    author_email='cindy@datanarra.com',
    url='http://github.com/cindyc/datanarra/modelgenie',
    install_requires=[requirements, dev_requirements],
    packages=['modelgenie', 'persistence', 'rest', 'carbon'],
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
