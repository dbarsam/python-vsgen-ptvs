# -*- coding: utf-8 -*-
"""
This module provides the neccessary project defintions for VSGDemo's PTVS projects
"""
import os
from vsgenptvs.interpreter import PTVSInterpreter
from vsgendemo.base import VSGDemoBaseProject
from vsgendemo.settings import VSGDemoSettings


class VSGProject(VSGDemoBaseProject):
    """
    VSGDemoProject provides a VSGProject for the main VSG project
    """
    RootPath = os.path.join(VSGDemoSettings.MainRoot, 'vsgen')

    def __init__(self, **kwargs):
        super(VSGProject, self).__init__('VSG', self.RootPath, **kwargs)

        if os.path.isdir(VSGDemoSettings.VE2Path):
            self.VirtualEnvironments.append(PTVSInterpreter.from_virtual_environment(VSGDemoSettings.VE2Path, VSVersion=self.VSVersion))
        if os.path.isdir(VSGDemoSettings.VE3Path):
            self.VirtualEnvironments.append(PTVSInterpreter.from_virtual_environment(VSGDemoSettings.VE3Path, VSVersion=self.VSVersion))

    def initialize(self):
        """
        Initializes the VSGProject by overriding the default values with instance specific values.
        """
        self.insert_files(self.RootPath)


class VSGDemoProject(VSGDemoBaseProject):
    """
    VSGDemoProject provides a VSGProject for the VSGDemo project
    """
    RootPath = os.path.join(VSGDemoSettings.MainRoot, 'tests', 'data', 'vsgendemo')

    def __init__(self, **kwargs):
        super(VSGDemoProject, self).__init__('VSGDemo', self.RootPath, **kwargs)

        if os.path.isdir(VSGDemoSettings.VE2Path):
            self.VirtualEnvironments.append(PTVSInterpreter.from_virtual_environment(VSGDemoSettings.VE2Path, VSVersion=self.VSVersion))
        if os.path.isdir(VSGDemoSettings.VE3Path):
            self.VirtualEnvironments.append(PTVSInterpreter.from_virtual_environment(VSGDemoSettings.VE3Path, VSVersion=self.VSVersion))

    def initialize(self):
        """
        Initializes the VSGProject by overriding the default values with instance specific values.
        """
        self.insert_files(self.RootPath)
