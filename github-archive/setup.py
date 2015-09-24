# -*- coding: utf-8; -*-
# vi: set encoding=utf-8

from setuptools import setup, find_packages

requirements = [
    'crate>=0.11.2',
    'tornado>=4.2',
]

setup(name='github-demo',
    version='0.1.0',
    url='https://github.com/crate/crate-demo',
    author='CRATE Technology GmbH',
    author_email='office@crate.io',
    license='Apache License 2.0',
    platforms=['any'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'import = s3tocrate:main',
            'webapp = webapp:server',
        ],
    },
    install_requires=requirements,
)

