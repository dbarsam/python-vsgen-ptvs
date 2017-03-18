==========
vsgen-ptvs
==========
|build-status| |docs| |dependencies| |pypi-version| |pypi-license| |python-2| |python-3|

A Python package that extends vsgen_ with solutions and project defintions for `Python Tools for Visual Studio`_.

Installation
============
Use pip: ::

  pip install vsgen-ptvs

Usage
=====
This package defines the vsgen_ ``ptvs`` type but follows the standard vsgen_ usage:

#. Manipulate the `vsgen-ptvs` provided classes directly with Python script and then generate the files using vsgen_'s commands.

#. Use the command line and supply a configuration file that contains the solution and project defintions and let vsgen_ automaticaly generate the files.

Documentation
=============
Documentation is available at `readthedocs.org <http://vsgen-ptvs.readthedocs.org/en/latest/>`_.

Support
=======
Use the `issue tracker <https://github.com/dbarsam/python-vsgen-ptvs/issues>`_ to file any suggestions, bugs or other issues.

.. _vsgen: http://vsgen.readthedocs.io
.. _python tools for visual studio: https://github.com/Microsoft/PTVS

.. |build-status| image:: https://ci.appveyor.com/api/projects/status/1wc3ljtcv0guswj7/branch/master?svg=true
    :alt: build status
    :scale: 100%
    :target: https://ci.appveyor.com/project/dbarsam/python-vsgen-ptvs

.. |docs| image:: https://readthedocs.org/projects/vsgen-ptvs/badge/?version=stable
    :alt: Documentation Status
    :scale: 100%
    :target: http://vsgen-ptvs.readthedocs.org/en/latest/

.. |dependencies| image:: https://img.shields.io/requires/github/dbarsam/python-vsgen-ptvs.svg
    :target: https://requires.io/github/dbarsam/python-vsgen-ptvs/requirements/
    :alt: Dependencies

.. |pypi-version| image:: http://img.shields.io/pypi/v/vsgen-ptvs.svg
    :alt: PyPI Version
    :scale: 100%
    :target: https://pypi.python.org/pypi/vsgen-ptvs

.. |pypi-license| image:: http://img.shields.io/pypi/l/vsgen-ptvs.svg
    :alt: PyPI License
    :scale: 100%
    :target: https://pypi.python.org/pypi/vsgen-ptvs

.. |python-2| image:: http://img.shields.io/badge/python-2-blue.svg
    :alt: Python 2 Compatible
    :scale: 100%

.. |python-3| image:: http://img.shields.io/badge/python-3-blue.svg
    :alt: Python 3 Compatible
    :scale: 100%

