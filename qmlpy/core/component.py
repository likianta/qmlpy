from __future__ import annotations

import typing as t
from secrets import token_hex
from textwrap import dedent
from textwrap import indent

from .declarative import Id
from .declarative import ctx_mgr
from .declarative import id_mgr
from .pyside import pyside

PropertyGroup = ...


class T:
    Component = t.TypeVar('Component', bound='Component')
    Level = int  # 1, 2, 3, ... see also `..declarative.id_system.Id`
    Properties = ...
    Signals = ...


class Component:
    id: Id
    
    def __enter__(self) -> t.Self:
        self.id = ctx_mgr.enter(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        ctx_mgr.leave()
    
    @property
    def widget_name(self):
        return self.__class__.__name__
    
    def build(self, level=0) -> str:
        return build_component(self, level)


def build_component(comp: T.Component, level: T.Level) -> str:
    def _loop(comp: T.Component):
        return dedent('''
            {widget_name} {{
                id: {id}
                objectName: "{qid}"

                {properties}

                {connections}

                {signals}

                {children}
            }}
        ''').strip().format(
            widget_name=comp.widget_name,
            id=comp.id,
            properties=indent(
                '\n'.join(sorted(build_properties(comp.properties))),
                '    '
            ).lstrip() or '// NO_PROPERTY_DEFINED',
            connections=indent(
                '\n'.join(sorted(build_connections(comp.properties))),
                '    '
            ).lstrip() or '// NO_CONNECTION_DEFINED',
            signals=indent(
                '\n'.join(sorted(build_signals(comp.signals))),
                '    '
            ).lstrip() or '// NO_SIGNAL_DEFINED',
            children=indent(
                '\n\n'.join(map(_loop, id_mgr.get_children(comp.qid))),
                '    '
            ).lstrip() or '// NO_CHILD_DEFINED',
        )
    
    out = indent(_loop(comp), ' ' * level)
    return out


def build_properties(props: T.Properties, group_name=''):
    for name, prop in props.items():
        # note prop type is Union[TProperty, TPropertyGroup], we should check
        # its type first.
        if isinstance(prop, PropertyGroup):
            yield from build_properties(prop.properties, prop.name)
        elif prop.value is None:
            continue
        else:
            # yield name, prop.value
            if group_name:
                yield '{}.{}: {}'.format(
                    group_name, _convert_name_case(name), prop.adapt()
                )
            else:
                yield '{}: {}'.format(_convert_name_case(name), prop.adapt())


def build_connections(props: T.Properties):
    for name, prop in props.items():
        if isinstance(prop, PropertyGroup):
            yield from build_connections(prop.properties)
        else:
            for notifier_name, func in prop.bound:
                if func is None:
                    yield '{}: {}'.format(
                        _convert_name_case(name),
                        _convert_name_case(notifier_name)
                    )
                else:
                    # assert isinstance(notifier_name, list)
                    pyside.register(
                        lambda *args: func(),
                        name=(random_id := token_hex(8))
                    )
                    yield '{}: pyside.call("{}", {})'.format(
                        _convert_name_case(name),
                        random_id,
                        list(map(_convert_name_case, notifier_name))
                    )


def build_signals(signals: T.Signals):
    for name, signal in signals.items():
        yield '{}: {}'.format(
            _convert_name_case(name),
            signal.adapt()
        )


def _convert_name_case(snake_case: str):
    """ snake_case to camelCase. For example, 'hello_world' -> 'helloWorld'. """
    if '.' in snake_case:
        # return '.'.join(_convert_name_case(s) for s in snake_case.split('.'))
        return '.'.join(map(_convert_name_case, snake_case.split('.')))
    
    if '_' not in snake_case:
        camel_case = snake_case
    else:
        segs = snake_case.split('_')
        camel_case = segs[0] + ''.join(x.title() for x in segs[1:])
    
    return camel_case
