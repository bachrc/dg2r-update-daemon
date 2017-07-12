import sys
import os
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='DG2R Armadillo Update Tool',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='GUI to sign and prepare updates for DG2R\'s Armadillos',
    long_description=long_description,

    # The project's main homepage.
    url='https://dg2r.fr',

    # Author details
    author='Yohann Bacha',
    author_email='bachrc@protonmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Maintainers of DG2R Armadillo\'s structure',
        'Topic :: Software Development :: Update Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='pgp update armadillo linux',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dg2r_update_daemon = update_tool.__main__:main'
        ]
    },
    install_requires=[
        'pycryptodome',
        'msgpack-python'
    ]
)
