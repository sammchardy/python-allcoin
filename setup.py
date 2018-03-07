#!/usr/bin/env python
from setuptools import setup

setup(
    name='python-allcoin',
    version='0.0.1',
    packages=['allcoin'],
    description='Allcoin REST API python implementation',
    url='https://github.com/sammchardy/python-allcoin',
    author='Sam McHardy',
    license='MIT',
    author_email='',
    install_requires=['requests', ],
    keywords='allcoin exchange rest api bitcoin ethereum btc eth qtum cnet ck.usd',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
