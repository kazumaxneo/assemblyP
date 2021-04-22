#!/usr/bin/env python3
"""
This is  
"""

import os
import shutil
import sys

from setuptools import setup
from setuptools.command.install import install


def readme():
    with open('README.md') as f:
        return f.read()


# Get the program version from another file.
__version__ = '0.3.0'
exec(open('assemblyP/version.py').read())

def parse_requirements():
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open('requirements.txt'))
    return [line for line in lineiter if line and not line.startswith("#")]

setup(name='assemblyP',
      version=__version__,
      description='assemblyP: a tool for designing primer at the end of contig',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/kazumax',
      author='Kazuma Uesaka',
      author_email='kazumax@gmail.com',
      license='GPLv3',
      packages=['assemblyP'],
      install_requires=parse_requirements(),
      entry_points={"console_scripts": ['assemblyP = assemblyP.__main__:main']},
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.6')

