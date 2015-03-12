# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

from setuptools import setup, find_packages

setup(
    name = 'gce-coreos',
    author = 'CrateIO',
    author_email = 'office@crate.io',
    namespace_packages = [],
    packages = find_packages('src'),
    package_dir = {'':'src'},
    install_requires = [
        'setuptools',
        ],
    entry_points = {
        'console_scripts': [
            'steps = sampledata:main'
            ]
        },
    include_package_data = True,
    zip_safe = True,
)

