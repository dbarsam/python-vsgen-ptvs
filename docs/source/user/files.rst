Configuration Files
===================

VSGen can use configuration files as input to its generation process.

VSGenPTVS defines additional section and options in a VSGen configuration file.

Sections
--------

Project Sections
~~~~~~~~~~~~~~~~
A `Python Tools for Visual Studio`_ project is identified by the ``ptvs`` type.

   .. code-block:: ini

	[vsgen.project.example]
	type = ptvs

ptvs options
^^^^^^^^^^^^
A `Python Tools for Visual Studio`_ project uses the following extra options.

.. contents::
   :local:
   :depth: 2

search_path
```````````
The comma separated list of absolute paths that define the project's Python search path.

startup_file
````````````
The absolute path of the project's startup file.

compile_files
`````````````
The comma separated list of initial files to be includes as compile files.

content_files
`````````````
The comma separated list of initial files to be includes as content files.
 
compile_in_filter
`````````````````
The comma separated list of :mod:`fnmatch` expressions (i.e. ``*.py``) used to include files automatically as compile files.

compile_ex_filter
`````````````````
The comma separated list of :mod:`fnmatch` expressions (i.e. ``*.py``) used to exclude files automatically from compile files.

content_in_filter
`````````````````
The comma separated list of :mod:`fnmatch` expressions (i.e. ``*.py``) used to include files automatically as content files.

content_ex_filter
`````````````````
The comma separated list of :mod:`fnmatch` expressions (i.e. ``*.py``) used to exclude files automatically from content files.

directory_in_filter
```````````````````
The comma separated list of path :mod:`fnmatch` expressions (i.e. ``out*``) used to include directories when autoamtically adding files.

directory_ex_filter
```````````````````
The comma separated list of path :mod:`fnmatch` expressions (i.e. ``out*``) used to exclude directories when autoamtically adding files.

is_windows_application
``````````````````````
Flag denoting if we're using python.exe or pythonw.exe as a launcher.

python_interpreter
``````````````````
The section defining the selected Python interpreters of this project.

python_interpreter_args
```````````````````````
The comman separated list of python interpreter arguments.

python_interpreters
```````````````````
The comma separated list of sections that define Python interpreters used by this project.

python_virtual_environments
```````````````````````````
The comma separated list of sections that define Python virtual environments used by this project.

Interpreter Section
~~~~~~~~~~~~~~~~~~~
A `Python Tools for Visual Studio`_ project uses one of more Python Interpreters.  Each interpretter could by a stanrad Python installation or a Pytyon virtual environment; however all interpreters are managed outside of Visual Studio and the projects include them as section references.

If the interpreter is a standard python interpreter the naming convention is ``[pyvsgen.interpreter.*]``.

If the interpreter is a virtual environment the naming convention is ``[vsgen.virtual_environment.*]``.

.. contents::
   :local:
   :depth: 2

Interpreter Options
^^^^^^^^^^^^^^^^^^^
A `Python Tools for Visual Studio`_ interpreter uses the following extra options.

interpreter_paths
`````````````````
The comma separated list of absolute paths that contain python installations.

description
```````````
The display description of the environment.

Virtual Environment options
^^^^^^^^^^^^^^^^^^^^^^^^^^^
A `Python Tools for Visual Studio`_ virtual environment uses the following extra options.

environment_paths
`````````````````
The comma separated list of absolute paths that contain virtual environments.

description
```````````
The display description of the interpreter.

Example
-------
The vsgen test suite contains an working example of a configuration file.  The file is available below and at :download:`setup.cfg <..\\..\\..\\tests\\data\\vsgencfg\\setup.cfg>`

.. literalinclude:: ..\..\..\tests\data\vsgencfg\setup.cfg

.. _Python Tools for Visual Studio: https://github.com/Microsoft/PTVS