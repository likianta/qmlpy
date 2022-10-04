"""
cheat with IDE type checking.

usage:
    from typehint import T as T0
    # create your own Typehint class
    class T:
        Component = T0.Component
        ...

notice:
    not suggest using inheritance `class T(T0)`, although it works.
"""
from typing import Any

__all__ = ['T']

if __name__ == '__main__':  # this is never reachable, just for type hint.
    class T:
        from qmlpy.component import Component  # noqa
        from qmlpy.declarative.id_system import Id  # noqa
        from qmlpy.properties.core import PropGroup  # noqa
        from qmlpy.properties.core import PropSheet  # noqa
        from qmlpy.properties.core import Property  # noqa
        from qmlpy.properties.core.prop_sheet import NotDefined  # noqa
else:
    T = ...


class FakeTypeGetter:
    def __getattr__(self, _) -> Any:
        return Any


globals()['T'] = FakeTypeGetter()
