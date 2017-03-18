Classes
=======
VSGen provides a collection of Python classes that represent solutions, projects, and other concepts used by Visual Studio to organise resources.

VSGenPTVS extends these classes with `Python Tools for Visual Studio`_ specializations.

Solutions
---------
Visual Studio currently uses one solution type so VSGen currently provides a single solution, the :class:`~vsgen.solution.VSGSolution` class.  VSGenPTVS does not define any solution classes.

Projects
--------

VSGenPTVS extends the base :class:`~vsgen.project.VSGProject` with the :class:`~vsgenptvs.project.PTVSProject` class that represents a `Python Tools for Visual Studio`_ ``.pyproj`` project file.

Suites
------
Suites are user defined groupings of solutions and projects.  VSGenPTVS extends the base :class:`~vsgen.suite.VSGSuite` with the :class:`~vsgenptvs.suite.PTVSSuite` class.  The :class:`~vsgenptvs.suite.PTVSSuite` class defines a simple solution and ``.pyproj`` project pair.

Other Classes
-------------

Python Tools for Visual Studio Interpreters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Python Tools for Visual Studio projects require a Python environment (or Python virtual environment) to exist on the user's machine and be `manually registered`_ with Visual Studio.  To automate this, each Python environment is represented by a :class:`~vsgenptvs.interpreter.PTVSInterpreter` class.

.. note:: The :class:`~vsgenptvs.interpreter.PTVSInterpreter` does not create or install a Python interpreter.  Instead it stores the Visual Studio specific definition of that environment and resolves the information for the project.  If the environment does not exist VSGen will throw an exception.

`Python Tools for Visual Studio`_ uses a Windows registry key to store Python environment information.  When VSGen processes an interpret object, it will do one of two things:

#. Create the respective Windows registry key.
#. Match the environment information against and existing Windows registry key.

In both cases however, VSGen ensures that that the project's environment will be recognised by Visual Studio.

Example
-------
The VSGenPTVS test suite contains an working example of using the objects in a demo package:

.. literalinclude:: ..\..\..\tests\data\vsgendemo\__main__.py

.. _Python Tools for Visual Studio: https://github.com/Microsoft/PTVS
.. _manually registered: https://github.com/Microsoft/PTVS/wiki/Python-Environments