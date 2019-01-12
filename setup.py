#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from setuptools import setup

from connectiontester import __program__, __version__, __description__


README = open('README.md').read()

# allow setup.py to be run from any path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

setup(
    name=__program__,
    version=__version__,
    license='MIT',
    description=__description__,
    long_description=README,
    url='https://github.com/AnselmC/connection-tester',
    author='Anselm Coogan',
    author_email='anselm.coogan@icloud.com',
    py_modules=['connectiontester', 'actionhandler', 'settings'],
    entry_points={
        'console_scripts': ['connectiontester=connectiontester:main']
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
)
