from __future__ import annotations

import typing as t

from .prop import Property
from .. import basic_types


class PropSheet:
    pass


class T:
    PropSheet = PropSheet
    Property = ...
    
    PropName = str
    PropType = str
    #   e.g. 'prop:Number'
    #   1. must start with 'prop:'
    #   2. there is no space between 'prop:' and the type name.
    #   3. the type name can be found in the list of `..basic_types`.
    SuperClasses = t.Iterator[t.Any]
    Target = t.Any
    
    PropFactory = t.Union[Property, t.Callable]
    #   either be a Property class, or an anonymous function that returns a
    #   Property class (which is `Delegate` or `AnyItem`).
    
    PropsIter = t.Iterator[t.Tuple[PropName, PropFactory]]


def init_prop_sheet(target: T.Target, prefix=''):
    """
    ref: https://stackoverflow.com/questions/2611892/how-to-get-the-parents-of-a
        -python-class
    """
    assert all((
        hasattr(target, 'id'),
        # hasattr(target, 'name'),
        hasattr(target, '_properties'),
    ))
    
    base_mixins = target.__class__.__bases__
    assert len(base_mixins) > 1 and issubclass(base_mixins[-1], PropSheet), (
        #  ^ assert 2+              ^ assert the final mixin is from PropSheet
        'target class must inherit from `PropSheet` (or its subclass) and you '
        'should put `PropSheet` as its last mixin.', target, base_mixins
    )
    
    for prop_name, prop_factory in _get_all_props(base_mixins[-1]):
        # noinspection PyProtectedMember
        target._properties[prop_name] = prop_factory(
            target.id, prefix + '.' + prop_name if prefix else prop_name
            #          ^ e.g. 'anchors.top'                    ^ e.g. 'width'
        )


def _get_all_props(target_class: T.PropSheet) -> T.PropsIter:
    if target_class is PropSheet:
        raise Exception(
            'this function can only be used for subclasses inherit from '
            '`PropSheet`, not for `PropSheet` itself!'
        )
    for cls in _get_base_classes(target_class):
        #   for example:
        #       class A:
        #           width = cast(int, 'prop:Number')
        for k, v in cls.__annotations__.items():
            if v.startswith('prop:'):
                #   k: str, property name. e.g. 'width'
                #   v: str, must start with 'prop:'. e.g. 'prop:Number'
                prop_name = k
                prop_factory = _get_actual_prop_class(v)
                yield prop_name, prop_factory


def _get_base_classes(cls: T.PropSheet) -> T.SuperClasses:
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


def _get_actual_prop_class(prop_type: T.PropType) -> T.PropFactory:
    if prop_type == 'prop:Property':
        return Property
    else:
        factory = getattr(basic_types, prop_type[5:])
        return factory
