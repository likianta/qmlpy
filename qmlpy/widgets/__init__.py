def __init__():
    """ setup widgets api. """
    from sys import path
    from lk_utils import relpath
    path.append(relpath('namespace'))
    
    from __qml_namespace__ import setup
    from . import widget_props
    from .. import properties
    from ..core import Component
    setup(component=Component,
          properties=properties,
          widget_properties=widget_props)


try:
    __init__()
except Exception as e:
    raise e
else:
    from .api import *
finally:
    del __init__
