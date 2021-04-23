#!/usr/bin/env python3

from setuptools import setup
import glob

scripts = glob.glob("*.p*")

setup(
    name='assemblyP',
    description='assemblyP: a tool for designing primer at the end of contig.',
    author='Kazuma Uesaka',
    author_email='kazumaxneo@gmail.com',
    packages=['assemblyP'],
    license='GPLv3',
    url='https://github.com/kazumax',
    package_dir={'assemblyP': 'assemblyP/'},
    entry_points={"console_scripts": ['assemblyP = assemblyP.__main__:main']},
    python_requires='>=3.6',
    install_requires=[
              'biopython',
          ],
    scripts=scripts,
    zip_safe=True
)





