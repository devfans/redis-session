#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis_session

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = """Simple tornado session implementation with redis store"""

setup(
    name='redis_session',
    version=redis_session.__VERSION__,
    description="Simple session implementation for Tornado",
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Programming Language :: Python :: 3',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='redis_session tornado web cookie session redis python',
    author="Stefan Liu",
    author_email="stefanliu@outlook.com",
    url="http://github.com/devfans/redis-session",
    license="MIT",
    packages=["redis_session"],
    include_package_data=True,
    zip_safe=True,
    install_requires=['tornado'],
)
