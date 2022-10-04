import typing as t

from qtpy.QtQuick import QQuickItem

from .common_util import snake_2_camel_case
from .prop_group import PropGroup


class T:
    from qtpy.QtCore import QObject
    Component = t.Any
    Root = t.Optional[QObject]


_root: T.Root = None


def build(qobj: T.QObject):
    # note: do not use collector to collect all qobjects, for example this is
    #   not correct:
    #       from ..control import id_mgr
    #       collector = {}
    #       for qid, _ in id_mgr.get_all_components():
    #           collector[qid] = qobj.findChild(QQuickItem, qid)
    #   because c++ internals will destroy all qobjects dynamically, the
    #   collector is hooking invalid qobjects.
    global _root
    _root = qobj


def getprop(
        comp: T.Component, key: str, default_value: t.Any
) -> t.Union['PropDelegate', PropGroup]:
    if not _root:
        return default_value
    if isinstance(default_value, PropGroup):
        return default_value
    qobj: T.QObject = _root.findChild(QQuickItem, comp.id)  # noqa
    try:
        return qobj.property(snake_2_camel_case(key))
    except RuntimeError:
        return PropDelegate(qobj, key)


def setprop(
        comp: T.Component, key: str, value: t.Any,
        default_set: t.Callable
) -> None:
    from ..group_types import Anchors
    from ...qmlside import qmlside
    
    if not _root:
        default_set(key, value)
        return
    
    if isinstance(value, PropGroup):
        raise Exception('This is not writable', comp, key, value)
    
    qobj: T.QObject = _root.findChild(comp.qid)  # noqa
    key: str = snake_2_camel_case(key)
    
    if isinstance(comp, PropGroup):
        group_name = snake_2_camel_case(comp.name)
        if isinstance(comp, Anchors):
            if key in ('centerIn', 'fill'):
                qmlside.bind_prop(qobj, f'{group_name}.{key}', value.qobj, '')
            else:
                qmlside.bind_prop(
                    qobj, f'{group_name}.{key}', value.qobj, value.prop)
        else:
            qmlside.bind_prop(
                qobj, f'{group_name}.{key}', value.qobj, value.prop)
    
    elif isinstance(value, PropDelegate):
        qmlside.bind_prop(qobj, key, value.qobj, value.prop)
    else:
        try:
            qobj.setProperty(key, value)
        except AttributeError:
            qmlside.bind_prop(qobj, key, value, '')


class PropDelegate:
    def __init__(self, qobj, prop):
        self.qobj = qobj
        self.prop = prop
