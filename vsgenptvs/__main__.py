# -*- coding: utf-8 -*-
"""
This module provides the main command line interface to using VSG.
"""

import os
import sys
import argparse


def make_documentation_parser(**kwargs):
    """
    Generates the application's :class:`~argparse.ArgumentParser` instance for the documentation generator `sphinx-argparse <https://sphinx-argparse.readthedocs.io>`_
    """
    from vsgen import VSGSuite
    return VSGSuite.make_parser(**kwargs)


def main(argv=None):
    """
    The entry point of the script.
    """
    from vsgen import __main__

    # Special case to use the sys.argv when main called without a list.
    if argv is None:
        argv = sys.argv

    argv.insert(1, 'auto')
    argv.insert(2, 'ptvs')
    return __main__.main(argv)

if __name__ == "__main__":
    # To use this package as an application we need to correct the sys.path
    module_path = os.path.dirname(os.path.realpath(__file__))
    package_path = os.path.normpath(os.path.join(module_path, os.pardir))
    try:
        sys.path[sys.path.index(package_path)] = package_path
    except ValueError:
        sys.path.append(package_path)

    sys.exit(main(sys.argv))
