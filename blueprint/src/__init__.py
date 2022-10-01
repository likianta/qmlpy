"""
terminology:
    package (pakg): the qml importable name. for example 'qtquick',
        'quick.controls', etc.
        we use all snake_case naming style across the whole project.
    component (comp): the qml type name. for example 'Item', 'Rectangle',
        'MouseArea', etc.
    property (prop): qml property name. for example 'border', 'border.width',
        'color', etc.

structure:
    package (pakg)
        component (comp)
            property (prop)
"""
from . import io
from . import qml_modules_indexing
from . import template_generator
