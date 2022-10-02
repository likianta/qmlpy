import typing as t
from typing import _UnionGenericAlias as UnionType  # noqa


class T:
    PropSheet = 'PropSheet'
    Property = ...
    
    PropName = str
    SuperClasses = t.Iterator[t.Any]
    Target = t.Any
    
    PropFactory = t.Union[Property, t.Callable]
    #   either be a Property class, or an anonymous function that returns a
    #   Property class (which is `Delegate` or `AnyItem`).
    RawType = t.Union[Property, UnionType]
    #   RawType could be a Property class (seldomly used), or a UnionType
    #   (mostly used), which is like this:
    #       `width = Union[int, float, Number]`
    #                ^^^^^ this is called "UnionType".
    #   there are >=2 elements in UnionType, the formers are primitive python
    #   types, the final one is a Property class.
    #   why we are using this?
    #       it helps IDE (or mypy) to perform static type checking and code
    #       completion.
    #       for example, if we use `width = Number`, the IDE cannot recognize
    #       `width += 1` as a valid statement.
    #   TODO (refactor): we can use `width = cast(Union[int, float], Number)`
    #    instead. it means width is actually a Number, but IDE will treat it as
    #    an int or float type.
    
    PropsIter = t.Iterator[t.Tuple[PropName, PropFactory]]


class PropSheet:
    pass


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
        #  ^ assert 2+              ^ assert the final mixin is PropSheet
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
        #           width: Union[int, float, Number]
        for k, v in cls.__annotations__.items():
            #   k: str, property name. e.g. 'width'
            #   v: T.RawType. the annotated type for the property. e.g.
            #       `Union[int, float, Number]`
            if not k.startswith('_'):
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


Delegate = ...  # TODO  # noqa


def _get_actual_prop_class(raw_type: T.RawType) -> T.PropFactory:
    if type(raw_type) is UnionType:
        # e.g. Union[float, Number]
        constructor = raw_type.__args__[-1]
        if constructor is Delegate:
            constructor = lambda id_, name: Delegate(
                id_, name, delegate=raw_type.__args__[-2]
            )
    else:
        constructor = raw_type
    return constructor
