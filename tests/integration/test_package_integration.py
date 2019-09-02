# -*- coding: utf-8 -*-
"""
This module provides all integration test for the package functionality.
"""
import sys
import os
import importlib
import shutil
import unittest
import logging
import subprocess
import sys


#: Local path to Python 2 Virtual Environment
PYTHON2_VE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', '_ve2'))

#: Local path to Python 3 Virtual Environment
PYTHON3_VE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', '_ve3'))


def setUpModule():
    """
    The module specific setUp method
    """
    logging.disable(logging.CRITICAL)

    # Create a Python 2 Virtual Environment
    try:
        import virtualenv
        # Note:  We can't create it from virtualenv API so launch an external process.
        subprocess.Popen([sys.executable, '-m', 'virtualenv', PYTHON2_VE], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    except ImportError:
        pass

    # Create a Python 3 Virtual Environment
    try:
        import venv
        venv.main([PYTHON3_VE])
    except ImportError:
        pass


def tearDownModule():
    """
    The module specific tearDown method
    """
    if os.path.isdir(PYTHON2_VE):
        shutil.rmtree(PYTHON2_VE)

    if os.path.isdir(PYTHON3_VE):
        shutil.rmtree(PYTHON3_VE)

    logging.disable(logging.NOTSET)


class TestIntegrationPackage(unittest.TestCase):
    """
    Tests the Solution and Project Generation from a python package file.
    """

    def setUp(self):
        """
        The class specific setUp method
        """
        self.assertTrue(os.path.isdir(PYTHON2_VE) or os.path.isdir(PYTHON3_VE), 'Test data\'s virtual environment(s) do not exist at {} or {}.'.format(PYTHON2_VE, PYTHON3_VE))

        self._data = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self.assertTrue(os.path.isdir(self._data), 'Test data directory "{}" does not exist'.format(self._data))

        self._output = os.path.normpath(os.path.join(self._data, '_output'))
        self.assertFalse(os.path.exists(self._output), 'Test output directory already exits!'.format(self._output))

        self._package = os.path.normpath(os.path.join(self._data, 'vsgendemo'))
        self.assertTrue(os.path.isdir(self._package), 'Test package "{}" does not exist'.format(self._package))

        # Append the to the sys path
        rootdir = os.path.dirname(self._package)
        if rootdir not in sys.path:
            sys.path.append(rootdir)

    def tearDown(self):
        """
        The class specific tearDown method
        """
        # Remove the package from the sys path
        rootdir = os.path.dirname(self._package)
        if rootdir in sys.path:
            sys.path.remove(rootdir)

        # Remove the output directory
        if os.path.exists(self._output):
            shutil.rmtree(self._output)

    def test_package_success(self):
        """
        Tests the expected workflow.
        """
        package_name = os.path.basename(self._package)
        main_module = importlib.import_module("{}.__main__".format(package_name))
        result = main_module.main()

        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
