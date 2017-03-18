# -*- coding: utf-8 -*-
"""
vsgen-ptvs's setup.py

For more details see https://packaging.python.org/en/latest/distributing/#setup-args
"""
from os import path
from setuptools import setup, find_packages
from codecs import open

ROOT_PATH = path.abspath(path.dirname(__file__))

INSTALL_REQUIREMENTS = [
    'vsgen'
]

TEST_REQUIREMENTS = [
    'vsgen',
    'pep8'
]

SETUP_REQUIREMENTS = [
    'setuptools-pep8',
    'setuptools-lint',
    'setuptools_scm'
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Topic :: Software Development ',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Topic :: Office/Business :: Groupware',
]

ENTRY_POINTS = {
    'console_scripts': [
        'vsgen-ptvs = vsgenptvs.__main__:main'
    ],
    'vsgen.suites': [
        'ptvs = vsgenptvs.suite:PTVSSuite'
    ],
    'vsgen.projects': [
        'ptvs = vsgenptvs.project:PTVSProject'
    ]
}

PACKAGES = find_packages(exclude=['contrib', 'docs', 'tests', '.eggs'])

README = open(path.join(ROOT_PATH, 'README.rst'), encoding='utf-8').read()

CHANGES = open(path.join(ROOT_PATH, 'CHANGES.rst'), encoding='utf-8').read()

LONG_DESCRIPTION = README + '\n\n' + CHANGES

PACKAGE_DIR = {
    'vsgenptvs': './vsgenptvs'
}

PACKAGE_DATA = {
    'vsgenptvs': ['data/*.*']
}

SCM_VERSION = {
    'local_scheme': 'dirty-tag'
}

setup(
    name='vsgen-ptvs',
    description='An extension for the VSGen solution and project generator that defines projects and solutions for Python Tools for Visual Studio.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/dbarsam/python-vsgen-ptvs',
    author='dbarsam',
    author_email='dbarsam@gmail.com',
    license='MIT',
    setup_requires=SETUP_REQUIREMENTS,
    classifiers=CLASSIFIERS,
    keywords='visual studio project generation',
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    package_data=PACKAGE_DATA,
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIREMENTS,
    use_scm_version=SCM_VERSION
)
