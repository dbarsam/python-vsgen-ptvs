# -*- coding: utf-8 -*-
"""
Main __init__.py for the vsgen-ptvs package
"""
import pkg_resources
try:
    pkg = pkg_resources.get_distribution("vsgen-ptvs")
    __version__ = pkg.version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0.0"

from vsgenptvs.interpreter import PTVSInterpreter
from vsgenptvs.project import PTVSProject
from vsgenptvs.suite import PTVSSuite

__all__ = [
    'PTVSInterpreter',
    'PTVSProject',
    'PTVSSuite'
]
