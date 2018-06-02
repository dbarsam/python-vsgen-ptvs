# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions to generate a Project File.
"""

import os
import pkg_resources

from vsgen.project import VSGProject
from vsgen.writer import VSGWritable, VSGJinjaRenderer
from vsgen.register import VSGRegisterable
from vsgenptvs.interpreter import PTVSInterpreter


class PTVSProject(VSGProject, VSGWritable, VSGRegisterable, VSGJinjaRenderer):
    """
    PTVSProject extends :class:`~vsgen.project.VSGProject` with data and logic needed to create a `.pyproj` file.

    :ivar list  SearchPath:             The list of absolute directories that will be added to the Python search path; if not provide the value is [].
    :ivar bool  IsWindowsApplication:   The boolean flag to launch the application as a `.pyw` file or not; if not provide the value is False.
    :ivar list  EnvironmentVariables:   The list of environment variables applied by the project; if not provide the value is [].
    :ivar list  PythonInterpreter:      The active interpreter. Either None or one of the values specified in PythonInterpreters or VirtualEnvironments; if not provide the value is None.
    :ivar list  PythonInterpreterArgs:  The active interpreter's arguments.  If not provide the value is [].
    :ivar list  PythonInterpreters:     The list of pyInterpreters that are base interpreters that will be available; if not provide the value is [].
    :ivar list  VirtualEnvironments:    The list of pyInterpreters that are virtual environments that will be available; if not provide the value is [].
    """
    __project_type__ = 'ptvs'

    __writable_name__ = "Visual Studio PTVS Project"

    __registerable_name__ = "Visual Studio PTVS Python Interpreter"

    __jinja_template__ = pkg_resources.resource_filename('vsgenptvs', 'data/ptvs.jinja')

    def __init__(self, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(PTVSProject, self).__init__(**kwargs)

    def _import(self, datadict):
        """
        Internal method to import instance variables data from a dictionary

        :param dict datadict: The dictionary containing variables values.
        """
        super(PTVSProject, self)._import(datadict)
        self.SearchPath = datadict.get("SearchPath", [])
        self.IsWindowsApplication = datadict.get("IsWindowsApplication", False)
        self.EnvironmentVariables = datadict.get("EnvironmentVariables", [])
        self.PythonInterpreter = datadict.get("PythonInterpreter", None)
        self.PythonInterpreterArgs = datadict.get("PythonInterpreterArgs", [])
        self.PythonInterpreters = datadict.get("PythonInterpreters", [])
        self.VirtualEnvironments = datadict.get("VirtualEnvironments", [])

    @classmethod
    def from_section(cls, config, section, **kwargs):
        """
        Creates a :class:`~vsgenptvs.interpreter.PTVSProject` from a :class:`~configparser.ConfigParser` section.

        :param ConfigParser config:   A :class:`~configparser.ConfigParser` instance.
        :param str          section:  A :class:`~configparser.ConfigParser` section key.
        :param              kwargs:   List of additional keyworded arguments to be passed into the :class:`~vsgenptvs.project.PTVSProject`.
        :return:                      A valid :class:`~vsgenptvs.project.PTVSProject` instance if succesful; None otherwise.
        """
        p = super(PTVSProject, cls).from_section(config, section, **kwargs)

        p.SearchPath = config.getdirs(section, 'search_path', fallback=p.SearchPath)
        p.IsWindowsApplication = config.getboolean(section, 'is_windows_application', fallback=p.IsWindowsApplication)
        p.EnvironmentVariables = config.getlist(section, 'environment_variables', fallback=p.EnvironmentVariables, delimiters='')
        p.PythonInterpreterArgs = config.getlist(section, 'python_interpreter_args', fallback=p.PythonInterpreterArgs)

        environment_sections = [es for es in p.EnvironmentVariables if config.has_section(es)]
        for es in environment_sections:
            p.EnvironmentVariables.remove(es)
            for o in config.options(es):
                p.EnvironmentVariables.append("{}={}".format(o, config.get(es, o, vars=os.environ)))

        interpreter = config.get(section, 'python_interpreter', fallback=None)
        interpreters = {n: [i for i in PTVSInterpreter.from_section(config, n, VSVersion=p.VSVersion)] for n in config.getlist(section, 'python_interpreters')}
        p.PythonInterpreters = [i for v in interpreters.values() for i in v]
        p.PythonInterpreter = next((i for i in interpreters.get(interpreter, [])), None)

        virtual_environments = config.getlist(section, 'python_virtual_environments', fallback=[])
        p.VirtualEnvironments = [ve for n in virtual_environments for ve in PTVSInterpreter.from_section(config, n, VSVersion=p.VSVersion)]

        return p

    @property
    def SearchPathRelative(self):
        """
        Returns the :attr:`SearchPath` relative to :attr:`ProjectHome` directory.
        """
        return [os.path.relpath(path, self.ProjectHome) for path in self.SearchPath] if self.SearchPath else [self.ProjectHome]

    @property
    def ProjectInterpreterDefault(self):
        """
        Returns the main Python interpretter, either :attr:`PythonInterpreter` or the first interpretter in :attr:`PythonInterpreters`.
        """
        return self.PythonInterpreter or next((p for p in self.PythonInterpreters), None)

    def write(self):
        """
        Creates the PTVS project file.
        """
        filters = {
            'MSGUID': lambda x: ('{%s}' % x).upper(),
            'relprojhome': lambda x: os.path.relpath(x, self.ProjectHome),
            'relprojfile': lambda x: os.path.relpath(x, self.FileName)
        }

        context = {
            'pyproj': self,
        }
        return self.render(self.__jinja_template__, self.FileName, context, filters)

    def register(self):
        """
        Registers the project's python environments.
        """
        # Interpretters
        for i in set(self.PythonInterpreters):
            i.register()
