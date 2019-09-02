# -*- coding: utf-8 -*-
"""
This module provides the necessary definitions to generate a Python Interpreter object.
"""

import os
import re
import csv
import site
import io
import fnmatch
import uuid
import subprocess
import configparser
try:
    import winreg
except ImportError:
    import _winreg as winreg
from vsgen.register import VSGRegisterable


class PTVSInterpreter(VSGRegisterable):
    """
    PTVSInterpreter encapsulates the logic and data used to describe a Python interpreter or virtual environments

    :ivar str  ID:                      The Visual Studio ID the Python Interpreter; if not provided one is generated automatically.
    :ivar str  Architecture:            The architecture (either x86 or x64). if not provide the value is "".
    :ivar str  Version:                 The major.minor version string; if not provide the value is "".
    :ivar str  Description:             The human readable description string; if not provide the value is ""
    :ivar str  Path:                    The absolute path of the `python.exe`; if not provide the value is ""
    :ivar str  InterpreterPath:         The relative path to self.Path of the `python.exe`; if not provide the value is ""
    :ivar str  WindowsInterpreterPath:  The relative path to self.Path of the `pythonw.exe`; if not provide the value is ""
    :ivar str  PathEnvironmentVariable: The name of the environment variable to be uses as `PYTHONPATH`; if not provide the value is "PYTHONPATH".
    """
    __registerable_name__ = "Python Interpreter"

    #: Official WIndows Registry Keys for Python environments.
    __global_interpreter_keys__ = [
        (winreg.HKEY_CURRENT_USER, r'Software\Python', winreg.KEY_WOW64_64KEY),
        (winreg.HKEY_CURRENT_USER, r'Software\Python', winreg.KEY_WOW64_32KEY),
        (winreg.HKEY_LOCAL_MACHINE, r'Software\Python', winreg.KEY_WOW64_64KEY),
        (winreg.HKEY_LOCAL_MACHINE, r'Software\Python', winreg.KEY_WOW64_32KEY),
    ]

    #: PTVS Custom Interpreter Registry Location
    __ptvs_interpreter_key__ = (winreg.HKEY_CURRENT_USER, r'Software\Python\VisualStudio', winreg.KEY_WOW64_64KEY)


    def __init__(self, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(PTVSInterpreter, self).__init__()
        self._import(kwargs)

    @staticmethod
    def python_architecture(interpreter):
        """
        Returns the architecture of the Python interpreter.

        :param str interpreter: Absolute path to `python.exe`.
        :return:                Either 'x86' or 'x64' if succesful; None otherwise.
        """
        try:
            out, err = subprocess.Popen([interpreter, '-c', 'import platform;print(\'x64\' if \'64bit\' in platform.architecture() else \'x86\')'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            return out.decode("utf-8").rstrip()
        except BaseException:
            return None

    @staticmethod
    def python_version(interpreter):
        """
        Returns the version of the Python interpreter.

        :param str interpreter: Absolute path to `python.exe`.
        :return:                The version text if succesful; None otherwise.
        """
        try:
            out, err = subprocess.Popen([interpreter, '-c', 'import sys;print(\'.\'.join(str(s) for s in sys.version_info[:2]))'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            return out.decode("utf-8").rstrip()
        except BaseException:
            return None

    @classmethod
    def from_section(cls, config, section, **kwargs):
        """
        Creates a :class:`~vsgenptvs.interpreter.PTVSInterpreter` from a :class:`~configparser.ConfigParser` section.

        :param obj config:   A :class:`~configparser.ConfigParser` instance.
        :param str section:  A :class:`~configparser.ConfigParser` section key.
        :param kwargs:       List of additional keyworded arguments to be passed into the :class:`~vsgenptvs.interpreter.PTVSInterpreter`.
        :return:             A valid :class:`~vsgenptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
        :note:               This function interprets the section either as a python interpreter or a virtual environment, not both.
        """
        if section not in config:
            raise ValueError('Section [{}] not found in [{}]'.format(section, ', '.join(config.sections())))

        interpreters = []
        interpreter_paths = config.getdirs(section, 'interpreter_paths', fallback=[])
        environment_paths = config.getdirs(section, 'environment_paths', fallback=[])
        if interpreter_paths:
            interpreter_objects = (PTVSInterpreter.from_python_installation(p, **kwargs) for p in interpreter_paths)
            interpreters = list(filter(None, interpreter_objects))
        elif environment_paths:
            interpreter_objects = (PTVSInterpreter.from_virtual_environment(p, **kwargs) for p in environment_paths)
            interpreters = list(filter(None, interpreter_objects))

        for i in interpreters:
            i.Description = config.get(section, 'description', fallback=i.Description)

        return interpreters

    @classmethod
    def from_virtual_environment(cls, directory, **kwargs):
        """
        Creates a :class:`~vsgenptvs.interpreter.PTVSInterpreter` from an Python Virtual Environment in the directory.

        :param str directory: The absolute path to the python virtual environment directory.
        :param kwargs:    List of additional keyworded arguments to be passed into the :class:`~vsgenptvs.interpreter.PTVSInterpreter`.
        :return:          A valid :class:`~vsgenptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
        """
        root = os.path.abspath(directory)
        python = os.path.abspath(os.path.join(root, 'Scripts', 'python.exe'))
        if not os.path.exists(python):
            return None

        root = os.path.abspath(directory)
        origprefix = os.path.abspath(os.path.join(root, 'Lib', 'orig-prefix.txt'))
        pyvenvcfg = os.path.abspath(os.path.join(root, 'pyvenv.cfg'))
        if not os.path.exists(origprefix) and not os.path.exists(pyvenvcfg):
            return None

        if os.path.exists(origprefix):
            with open(origprefix, 'rt') as f:
                basedir = next((line.rstrip() for line in f), None)

        if os.path.exists(pyvenvcfg):
            with io.open(pyvenvcfg, encoding='utf-8') as f:
                for line in f:
                    if '=' in line:
                        key, _, value = line.partition('=')
                        key = key.strip().lower()
                        value = value.strip()
                        if key == 'home':
                            basedir = value

        args = kwargs.copy()
        args['Path'] = root
        args['ID'] = os.path.basename(root)
        args['InterpreterPath'] = os.path.join('Scripts', 'python.exe')

        if os.path.exists(os.path.join(root, 'Scripts', 'pythonw.exe')):
            args['WindowsInterpreterPath'] = os.path.join('Scripts', 'pythonw.exe')

        version = cls.python_version(python)
        if version:
            args['Version'] = version

        architecture = cls.python_architecture(python)
        if architecture:
            args['Architecture'] = architecture

        args['Description'] = '{} (Python {} ({}))'.format(os.path.basename(root), args.get('Version', 'Unknown'), args.get('Architecture', 'Unknown'))

        interpreter = cls(**args)
        return interpreter

    @classmethod
    def from_python_installation(cls, directory, **kwargs):
        """
        Creates a :class:`~vsgenptvs.interpreter.PTVSInterpreter` from an Python installation in the directory.

        :param str directory: The absolute path to the python installation directory.
        :param kwargs:  List of additional keyworded arguments to be passed into the :class:`~vsgenptvs.interpreter.PTVSInterpreter`.
        :return:          A valid :class:`~vsgenptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
        """

        # First check the installations in the registry
        interpreter = cls.from_registry_installation(directory, **kwargs)
        if interpreter:
            return interpreter

        # Manually Create
        root = os.path.abspath(directory)
        python = os.path.abspath(os.path.join(root, 'python.exe'))
        if not os.path.exists(python):
            return None

        args = kwargs.copy()
        args['Path'] = root
        args['InterpreterPath'] = 'python.exe'
        args.setdefault('Description', os.path.basename(root))

        if os.path.exists(os.path.join(root, 'pythonw.exe')):
            args['WindowsInterpreterPath'] = 'pythonw.exe'

        version = cls.python_version(python)
        if version:
            args['Version'] = version

        architecture = cls.python_architecture(python)
        if architecture:
            args['Architecture'] = architecture

        interpreter = cls(**args)
        return interpreter

    @classmethod
    def from_registry_installation(cls, directory, **kwargs):
        """
        Creates a :class:`~vsgenptvs.interpreter.PTVSInterpreter` from an Python installation in the registered in the Windows registry.

        :param str directory: The absolute path to the python installation directory.
        :param kwargs:  List of additional keyworded arguments to be passed into the :class:`~vsgenptvs.interpreter.PTVSInterpreter`.
        :return:   A valid :class:`~vsgenptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
        """
        def enum_keys(key):
            i = 0
            while True:
                try:
                    yield winreg.EnumKey(key, i)
                except OSError:
                    break
                i += 1

        path = os.path.normpath(directory).lower()
        for hive, key, flag in cls.__global_interpreter_keys__:
            with winreg.OpenKeyEx(hive, key, access=winreg.KEY_READ | flag) as root_key:
                for company in enum_keys(root_key):
                    with winreg.OpenKey(root_key, company) as company_key:
                        for tag in enum_keys(company_key):
                            interpreter = cls.from_registry_key(hive, os.path.join(key, company, tag), flag, **kwargs)
                            if interpreter and interpreter.Path.lower() == path:
                                return interpreter
        return None

    @classmethod
    def from_registry_key(cls, hive, key, flag, **kwargs):
        """
        Creates a :class:`~vsgenptvs.interpreter.PTVSInterpreter` from a PEP-514 `registry key <https://www.python.org/dev/peps/pep-0514>`_.

        :param obj hive:  One of the `HKEY constants <https://docs.python.org/3/library/winreg.html#hkey-constants>`_.
        :param str key:   The keyname under `hive` referring to the Python environment.
        :param int flag:  The windows registry access mask value.
        :param kwargs:  List of additional keyworded arguments to be passed into the :class:`~vsgenptvs.interpreter.PTVSInterpreter`.
        :return:          A valid :class:`~vsgenptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
        """
        tag = os.path.basename(key)
        company = os.path.basename(os.path.dirname(key))

        regkeys = {
            key : [
                'SysArchitecture',
                'SysVersion',
                'Version',
                'SupportUrl',
                'DisplayName'
            ],
            os.path.join(key, 'InstallPath') : [
                'ExecutablePath',
                'ExecutableArguments',
                'WindowedExecutablePath',
                'WindowedExecutableArguments'
            ]
        }

        mapping = {
            'Architecture':'SysArchitecture',
            'Version':'SysVersion',
            'PathEnvironmentVariable' : 'PathEnvironmentVariable',
            'Description' : 'DisplayName',
            'InterpreterPath': 'ExecutablePath',
            'WindowsInterpreterPath' : 'WindowedExecutablePath'
        }

        regvalues = {}
        for regkey, value_names in regkeys.items():
            with winreg.OpenKeyEx(hive, regkey, access=winreg.KEY_READ | flag) as subkey:
                for value_name in sorted(value_names):
                    try:
                        regvalues[value_name], _ = winreg.QueryValueEx(subkey, value_name)
                    except FileNotFoundError as e:
                        regvalues[value_name] = None
        args = {}
        for k, v in  mapping.items():
            if v in regvalues and regvalues[v]:
                args[k] = regvalues[v]

        args['ID'] = "Global|{}|{}".format(company, tag)
        if 'InterpreterPath' in args:
            args['Path'] = os.path.dirname(args['InterpreterPath'])

        args.update(kwargs)

        return cls(**args)


    def _import(self, datadict):
        """
        Internal method to import instance variables data from a dictionary.

        :param dict datadict: The dictionary containing variables values.
        """
        self.ID = datadict.get('ID', "")
        self.Architecture = datadict.get('Architecture', "")
        self.Version = datadict.get('Version', "")
        self.Path = datadict.get('Path', "")
        self.Description = datadict.get('Description', "")
        self.InterpreterPath = datadict.get('InterpreterPath', "")
        self.InterpreterAbsPath = datadict.get('InterpreterAbsPath', self.InterpreterPath if os.path.isabs(self.InterpreterPath) else os.path.abspath(os.path.join(self.Path, self.InterpreterPath)))
        self.WindowsInterpreterPath = datadict.get('WindowsInterpreterPath', "")
        self.WindowsInterpreterAbsPath = datadict.get('WindowsInterpreterAbsPath', self.WindowsInterpreterPath if os.path.isabs(self.WindowsInterpreterPath) else os.path.abspath(os.path.join(self.Path, self.WindowsInterpreterPath)))
        self.PathEnvironmentVariable = datadict.get('PathEnvironmentVariable', "PYTHONPATH")
        self.VSVersion = datadict.get('VSVersion', None)

    def register(self):
        """
        Registers the environment into the windows registry.

        :note: We're explictly writing the environment to the registry to facilitate sharing. See `How to share pyproj across team with custom environments <https://pytools.codeplex.com/workitem/2765>`_ for motivation.
        """
        hive, key, flag = self.__ptvs_interpreter_key__
        tag = self.Description
        keyvalues = {
            os.path.join(key, tag) : {
                'SysArchitecture' : self.Architecture,
                'SysVersion' : self.Version,
                'DisplayName' : self.Description,
                'PathEnvironmentVariable' : 'PYTHONPATH'
            },
            os.path.join(key, tag, 'InstallPath') : {
                'ExecutablePath' :self.InterpreterAbsPath,
                'WindowedExecutablePath': self.WindowsInterpreterAbsPath,
            }
        }
        try:
            for key, values in keyvalues.items():
                with winreg.CreateKeyEx(hive, key, access=winreg.KEY_WRITE | flag) as regkey:
                    for k, v in values.items():
                        winreg.SetValueEx(regkey, k, 0, winreg.REG_SZ, v)
        except WindowsError:
            return False
        self.ID = "Global|VisualStudio|{}".format(company, tag)
        return True