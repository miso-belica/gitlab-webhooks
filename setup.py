# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import glhooks


with open("README.rst") as readme:
    with open("CHANGELOG.rst") as changelog:
        long_description = readme.read() + "\n\n" + changelog.read()


setup(
    name="glhooks",
    version=glhooks.__version__,
    description="Service for automatic updating of git repositories from GitLab.",
    long_description=long_description,
    author="Michal Belica",
    author_email="miso.belica@gmail.com",
    url="https://github.com/miso-belica/gitlab-webhooks",
    license="Apache License, Version 2.0",
    keywords=[
        "Git",
        "GitLab",
        "webhook",
        "hook",
    ],
    install_requires=[
        "docopt>=0.6.1,<0.7",
    ],
    tests_require=[
        "nose",
        "coverage",
    ],
    test_suite="nose.collector",
    packages=[
        "glhooks",
        "glhooks.mailer",
    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",

        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",

        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Version Control",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
