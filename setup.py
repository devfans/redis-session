#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado_redis_session

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = """Simple tornado session implementation with redis store"""

setup(
    name='tornado_redis_session',
    version=tornado_redis_session.__VERSION__,
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
    keywords='tornado_redis_session tornado web cookie session redis python',
    author="Stefan Liu",
    author_email="stefanliu@outlook.com",
    url="http://github.com/devfans/tornado-session",
    license="MIT",
    packages=["tornado_redis_session"],
    include_package_data=True,
    zip_safe=True,
    install_requires=['tornado',],
)
