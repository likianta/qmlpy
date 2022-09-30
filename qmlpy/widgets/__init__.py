from . import api


def __init__():
    """ setup widgets api. """
    from sys import path
    from lk_utils import relpath
    path.append(relpath('namespace'))
    
    from __qml_namespace__ import setup
    from . import properties
    from .widgets import Component
    from .widgets import widget_sheet
    setup(component=Component,
          properties=properties,
          widgets_sheet=widget_sheet)


__init__()
