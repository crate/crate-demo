
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='eden-facedetect',
    author='Claus Matzinger',
    author_email='claus@crate.io',
    description='Face detection for the Eden IoT platform',
    entry_points={
        'console_scripts': [
            'capture = eden.__main__:main',
#            'calibrate = eden.__main__:calibrate',
        ]
    },
    packages=['eden'],
    install_requires=[
        'picamera',
        'pyjwt',
        'argh',
        'toml'
    ],
    extras_require={
        'uvloop': ['uvloop'],
    },
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm']
)
