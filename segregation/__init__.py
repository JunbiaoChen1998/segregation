"""
:mod:`segregation` --- Spatial/Aspatial Segregation Analysis
=================================================

"""
from . import batch, decomposition, dynamics, inference, local, multigroup, singlegroup, util


# below handles deprecation warnings. Remove in 2.2.0
from . import  aspatial, spatial

from . import _version
__version__ = _version.get_versions()['version']
