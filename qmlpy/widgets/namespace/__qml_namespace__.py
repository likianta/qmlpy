"""
see `../__init__.py`.
"""
qml_namespace = set()  # type: set[str]

if __name__ == '__main__':  # this is never reachable. just for type hint.
    from qmlpy.core import Component as _Component
    from qmlpy.widgets import widget_props as _wprops
    from qmlpy import property as _property
    C = _Component
    P = _property
    W = _wprops
else:
    C = ...
    P = ...
    W = ...


def setup(**kwargs) -> None:
    global C, P, W
    C = kwargs['component']
    P = kwargs['properties']
    W = kwargs['widgets_sheet']
