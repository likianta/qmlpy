"""
see `../__init__.py`.
"""
__all__ = ['C', 'P', 'W', 'qml_namespace', 'setup']


class T:  # a fake typehint class, cheat with IDE type checking.
    if __name__ == '__main__':
        from qmlpy.component import Component
        from qmlpy.widgets import widget_props
        
        class PropsVendor:
            from qmlpy.properties.core import PropSheet
            PropSheet = PropSheet
    
    def __class_getitem__(cls, item):
        return None


qml_namespace = set()  # type: set[str]

C = T.Component
P = T.PropsVendor
W = T.widget_props

""" C: class Component.
    P: properties package. the only usage is `P.PropSheet`. see also
        `qmlpy.properties.core.prop_sheet.PropSheet`.
    W: widget oriented properties. we have implemented a list of detailed
        properties for EACH widget (that is a very long list, heavily auto-
        generated by blueprint). using `W.Ps<WidgetName>` to get the list.
"""


def setup(**kwargs) -> None:
    global C, P, W
    C = kwargs['component']
    P = kwargs['properties']
    W = kwargs['widget_properties']
