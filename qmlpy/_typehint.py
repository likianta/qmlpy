"""
cheat with IDE type checking.

usage:
    from typehint import T as T0
    # create your own T class
    class T:
        Component = T0.Component
        ...

notice:
    not suggest using inheritance `class T(T0)`, although it works.
"""
from typing import Any

if __name__ == '__main__':  # this is never reachable, just for type hint.
    class T:
        from qmlpy.component import Component  # noqa
        from qmlpy.declarative.id_system import Id  # noqa
        from qmlpy.properties.core import PropGroup  # noqa
        from qmlpy.properties.core import Property  # noqa


class FakeTypeGetter:
    def __getattr__(self) -> Any:
        return Any


globals()['T'] = FakeTypeGetter()
