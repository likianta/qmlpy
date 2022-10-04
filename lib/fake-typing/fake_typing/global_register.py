"""
usage:
    # test.py
    from fake_typing import register_fake_typing
    if register_fake_typing is None:
        # this is never reachable, just for type hint.
        class T:
            from qmlpy.component import Component
            from qmlpy.declarative.id_system import Id
            ...
    register_fake_typing('T')
    
how it works:
    `register_fake_typing` will register the name `T` to the global scope. the
    IDE will recognize it as `T` object, but that actually is `faker` object
    (see `./fake_type_getter.py > faker`).
"""

from inspect import currentframe

from .fake_type_getter import faker


def register_fake_typing(name: str = 'T'):
    frame = currentframe().f_back
    frame.f_globals[name] = faker
