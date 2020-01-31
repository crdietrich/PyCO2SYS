# PyCO2SYS: Python implementation of CO2SYS.
# Copyright (C) 2020  Matthew Paul Humphreys  (GNU GPLv3)
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name = 'PyCO2SYS',
    version = '0.1',
    author = 'Matthew P. Humphreys',
    author_email = 'm.p.humphreys@icloud.com',
    description = 'Python implementation of CO2SYS',
    url = 'https://github.com/mvdh7/PyCO2SYS',
    packages = setuptools.find_packages(),
    install_requires = [
        'numpy>=1.15',
    ],
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
)
