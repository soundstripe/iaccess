#!/usr/bin/env python

"""The setup script."""
import re
from pathlib import Path

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

version_file = Path('iaccess/__init__.py')
version = re.match(
    r""".*__version__ = '(.*?)'""", version_file.read_text(), re.S
).group(1)

requirements = ['sqlalchemy', 'pyodbc!=4.0.30']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Steven Clayton James",
    author_email='steven@waitforitjames.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Database',
    ],
    description="Provides support for DB2 for iSeries for remote python clients "
                "using IBM i Access Client Solutions ODBC driver",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='iaccess',
    name='iaccess',
    packages=find_packages(include=['iaccess', 'iaccess.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/soundstripe/iaccess',
    version=version,
    zip_safe=False,
    entry_points={
     'sqlalchemy.dialects': [
          'iaccess.pyodbc = iaccess.dialect:IAccessDialect',
          'iaccess = iaccess.dialect:IAccessDialect',
          ]
    }
)
