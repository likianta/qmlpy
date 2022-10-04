"""
usage:
    from fake_typing import fake_typing
    
    @fake_typing
    class T:
        if fake_typing is None:
            # this is never reachable, just for type hint.
            from qmlpy.component import Component
            from qmlpy.declarative.id_system import Id
            ...
        __attrs__ = ['Component', 'Id', ...]  # list or tuple of attr names.
        
the decorator will register all elements in `T.__attrs__` to `T.__dict__`. so
you can use `T.Component` in your code, the IDE will recognize it as Component
object, but that actually is `typing.Any`.
this trick is used to cheat with IDE type checking, but avoid circular import
problem.
"""
from typing import Any


def fake_typing(cls):
    for k in cls.__attrs__:
        setattr(cls, k, Any)
    return cls
