Introduction
============

VSGenPTVS is a plugin to the VSGen that generates `Python Tools for Visual Studio <https://github.com/Microsoft/PTVS>`_ projects.

Install
-------
The package is designed to work with pip.

To install the package::

   pip install vsgenptvs

To uninstall the package::

   pip uninstall vsgenptvs

To upgrade the package::

   pip install --upgrade vsgenptvs
   
Starting with Python 2.7.9, pip is included by default with the Python binary installers.

Quick Start
-----------
VSGenPTVS adds the ``ptvs`` type to VSGen's ``auto`` command::

	vsgen auto ptvs <type options>

For example, to create a PTVS solution and project pointing at path ``S:\project`` named ``demo``::

	vsgen auto ptvs --root S:\project --name demo

Usage
-----
There are two ways to use vsgenptvs:

#. Creating objects explicitly using Python code and the vsgen base application.
#. Defining vsgenptvs objects using one or more configuration file and processing it with VSGen on the command line.
    
Using Python Code
~~~~~~~~~~~~~~~~~
VSGenPTVS extends the base classes and implementes the interfaces defined in VSGen.  More information is available on the :doc:`objects <objects>` page.

Command Line
~~~~~~~~~~~~

Using Configuration Files
*************************
VSGenPTVS makes the ``ptvs`` type availabel in VSGen's configuration file framework.

Automatic Generation
********************
VSGenPTVS makes the ``ptvs`` type availabel in VSGen's auto command line command.

Execution
---------
VSGenPTVS extends the VSGen command line but also creates an entry point for itself.

You can run it as a module::

	$ python -m vsgenptvs ...
    
which is equivalent to::

	$ python -m vsgen auto ptvs ...

Or, when installed with setuptools, run the auto generated entry point in Scripts::

	$ vsgen-ptvs ...

which is equivalent to::

	$ vsgen auto ptvs ...

Command Line Reference
~~~~~~~~~~~~~~~~~~~~~~

VSGenPTVS extends the existing VSGen command line but also provides its own command line handling.

VSGenPTVS Standalone
********************
When the ``vsgenptvs`` package is executed it passes the arguments to the command ``vsgen auto ptvs``  and presents the command line of that command as its own:

.. argparse::
    :ref: vsgenptvs.__main__.make_parser
    :prog: vsgenptvs


VSGen Command Line Integration
******************************
When ``vsgenptvs`` is installed, ``vsgen``'s command line is modified accordingly:

.. argparse::
    :ref: vsgen.__main__.make_documentation_parser
    :prog: vsgen


Getting help
------------

Check out the :doc:`FAQ <faq>` or submit a bug report to the `Github issue tracker <https://github.com/dbarsam/python-vsgen-ptvs/issues>`_.
