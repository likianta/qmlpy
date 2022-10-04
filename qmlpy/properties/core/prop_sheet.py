from __future__ import annotations

import typing as t
from dataclasses import dataclass

from fake_typing import register_fake_typing

if register_fake_typing is None:
    # this is never reacable. just for cheating with IDE.
    class T:
        from qmlpy.properties.core import NotDefined
        from qmlpy.properties.core import PropGroup
        from qmlpy.properties.core import PropSheet
        
        PropName = str
        PropType0 = str
        #   e.g. 'prop:Number'
        #   1. must start with 'prop:'
        #   2. there is no space between 'prop:' and the type name.
        #   3. the type name can be found in the list of `..basic_types`.
        PropType1 = t.Union[NotDefined, PropGroup]
        
        Properties0 = t.Dict[PropName, PropType1]
        # Properties1 = t.Iterator[
        #     t.Tuple[PropName, t.Union[T0.NotDefined, t.Any, T0.PropGroup]]]
        Properties1 = t.Dict[PropName, t.Union[NotDefined, t.Any, PropGroup]]
        AllPropertiesResult = t.Iterator[t.Tuple[PropName, PropType1]]
        
        SubInstanceOfPropSheet = PropSheet
        SubClassOfPropSheet = t.Type[PropSheet]
        SuperClasses = t.Iterator[SubInstanceOfPropSheet]
else:
    register_fake_typing('T')


class PropSheet:
    _properties: T.Properties0
    
    def __init__(self):
        self._init_properties()
    
    def _init_properties(self) -> None:
        self._properties = init_prop_sheet(self)
        for k, v in self._properties.items():
            setattr(self, k, v)
    
    @property
    def properties(self) -> T.Properties1:
        from .prop_group import PropGroup
        out = {}
        for k, v in self._properties.items():
            if isinstance(v, PropGroup):
                out[k] = v
            else:
                real_v = getattr(self, k)
                if isinstance(real_v, NotDefined):
                    out[k] = None
                else:
                    out[k] = real_v
        return out


@dataclass
class NotDefined:
    meta_prop: str


def init_prop_sheet(target: T.SubInstanceOfPropSheet) -> T.Properties0:
    """
    notice: target is an instance of a subclass of PropSheet.
    ref: https://stackoverflow.com/questions/2611892/how-to-get-the-parents-of-a
        -python-class
    """
    if target.__class__ is PropSheet:
        return {}
    
    base_mixins = target.__class__.__bases__
    assert len(base_mixins) > 1 and issubclass(base_mixins[-1], PropSheet), (
        #  ^ assert 2+              ^ assert the final mixin is from PropSheet
        'target class must inherit from `PropSheet` (or its subclass) and you '
        'should put `PropSheet` as its last mixin.',
        target.__name__, [x.__name__ for x in base_mixins]
    )
    
    properties: T.Properties0 = {}
    # noinspection PyTypeChecker
    for prop_name, prop_type in _get_all_props(base_mixins[-1]):
        properties[prop_name] = prop_type
    return properties


def _get_all_props(
        target_class: T.SubClassOfPropSheet
) -> T.AllPropertiesResult:
    from .. import group_types
    
    prop_name: T.PropName
    prop_type: T.PropType1
    
    for cls in _get_base_classes(target_class):
        #   the `cls` is from `...widgets.widget_props`.
        #   for example:
        #       class A:
        #           width = cast(int, 'prop:Number')
        for k, v in cls.__dict__.items():
            if isinstance(v, str) and v.startswith('prop:'):
                #   k: str, property name. e.g. 'width'
                #   v: str, must start with 'prop:'. e.g. 'prop:Number'
                prop_name = k
                if v[5:] in group_types.index:
                    prop_type = getattr(group_types, v[5:])()
                else:
                    prop_type = NotDefined(v[5:])
                yield prop_name, prop_type


def _get_base_classes(cls: T.SubClassOfPropSheet) -> T.SuperClasses:
    """
    args:
        cls: a subclass of PropSheet.

    example:
        class PropSheet: ...
        class A(PropSheet): ...
        class B(A): ...

        cls = B -> returns [B, A]
    """
    temp_cls = cls
    while issubclass(temp_cls, PropSheet):
        yield temp_cls
        temp_cls = temp_cls.__base__
