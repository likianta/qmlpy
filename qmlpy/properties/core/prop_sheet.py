from __future__ import annotations

import typing as t

from .. import group_types
from ..._typehint import T as T0


class T:
    Component = T0.Component
    PropName = str
    PropType = str
    #   e.g. 'prop:Number'
    #   1. must start with 'prop:'
    #   2. there is no space between 'prop:' and the type name.
    #   3. the type name can be found in the list of `..basic_types`.
    
    Properties = t.Dict[PropName, t.Optional[T0.PropGroup]]
    PropsIter = t.Iterator[t.Tuple[PropName, t.Optional[T0.PropGroup]]]
    
    SubClassOfPropSheet = t.Type[T0.PropSheet]
    SuperClasses = t.Iterator[SubClassOfPropSheet]


class PropSheet:
    properties: T.Properties
    
    def __init__(self):
        init_prop_sheet(self.__class__)


def init_prop_sheet(target_class: T.SubClassOfPropSheet) -> None:
    """
    ref: https://stackoverflow.com/questions/2611892/how-to-get-the-parents-of-a
        -python-class
    """
    if target_class is PropSheet:
        return
    
    base_mixins = target_class.__class__.__bases__
    assert len(base_mixins) > 1 and issubclass(base_mixins[-1], PropSheet), (
        #  ^ assert 2+              ^ assert the final mixin is from PropSheet
        'target class must inherit from `PropSheet` (or its subclass) and you '
        'should put `PropSheet` as its last mixin.', target_class, base_mixins
    )
    
    properties: T.Properties = {}
    # noinspection PyTypeChecker
    for prop_name, prop_type in _get_all_props(base_mixins[-1]):
        properties[prop_name] = prop_type
    setattr(target_class, 'properties', properties)


def _get_all_props(target_class: T.SubClassOfPropSheet) -> T.PropsIter:
    # if target_class is PropSheet:
    #     raise Exception(
    #         'this function can only be used for subclasses inherit from '
    #         '`PropSheet`, not for `PropSheet` itself!'
    #     )
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
                    prop_type = None
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
