"""
see `../__init__.py`.
"""
qml_namespace = set()

if __name__ == '__main__':  # this is never reachable. just for type hint.
    from qmlpy.widgets.base import Component as _Component
    from qmlpy.widgets import widget_sheet as _wsheet
    from qmlpy import properties as _properties
    C = _Component
    P = _properties
    W = _wsheet
else:
    C = ...
    P = ...
    W = ...


def setup(**kwargs):
    global C, P, W
    C = kwargs['component']
    P = kwargs['properties']
    W = kwargs['widgets_sheet']
