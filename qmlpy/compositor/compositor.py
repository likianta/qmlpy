import textwrap
import typing as t
from secrets import token_hex

from lk_utils import dumps

from .._typehint import T as T0
from ..declarative import id_mgr

__all__ = ['build_component', 'build_tree']

dedent = lambda x: textwrap.dedent(x).strip()
indent = textwrap.indent


class T:
    Component = T0.Component
    Properties = t.Dict[str, t.Union[T0.PropGroup, T0.Property, None]]
    Signals = t.Dict[str, t.Any]  # TODO


class Template:
    QmlFileScaffold = dedent('''
        {head}
        
        {body}
    ''')
    WidgetBlock = dedent('''
        {widget_name} {{
            id: {id}
            objectName: "{object_name}"

            {properties}

            {connections}

            {signals}

            {children}
        }}
    ''')


def build_tree(file_o: str) -> None:
    root_comp = id_mgr.get_component(id_mgr.root_id)
    body = _build_loop(root_comp, level=1)
    file_data = Template.QmlFileScaffold.format(
        head=...,  # TODO
        body=body
    )
    dumps(file_data, file_o)


def build_component(comp: T.Component, level: int = None) -> str:
    return _build_loop(comp, level or comp.level)


def _build_loop(comp: T.Component, level: int) -> str:
    out = dedent(Template.WidgetBlock.format(
        widget_name=comp.widget_name,
        id=f'u{comp.id}',
        object_name='{}#{}'.format(comp.widget_name, comp.id),
        properties=indent(
            '\n'.join(sorted(_build_properties(comp.properties))),
            '    '
        ).lstrip() or '// NO_PROPERTY_DEFINED',
        connections=indent(
            '\n'.join(sorted(_build_connections(comp.properties))),
            '    '
        ).lstrip() or '// NO_CONNECTION_DEFINED',
        signals=indent(
            '\n'.join(sorted(_build_signals(comp.signals))),
            '    '
        ).lstrip() or '// NO_SIGNAL_DEFINED',
        children=indent(
            '\n\n'.join(map(_build_loop, id_mgr.get_children(comp.id))),
            '    '
        ).lstrip() or '// NO_CHILD_DEFINED',
    ))
    out = indent(out, ' ' * (level - 1) * 4)
    return out


def _build_properties(props: T.Properties, group_name='') -> t.Iterator[str]:
    from ..properties.core import PropGroup
    for name, prop in props.items():
        if prop is None:
            continue
        elif isinstance(prop, PropGroup):
            yield from _build_properties(prop.properties, group_name=name)
        else:  # isinstace(prop, Property)  # TODO
            # yield name, prop.value
            if group_name:
                yield '{}.{}: {}'.format(
                    group_name, _snake_2_camel_case(name), prop.adapt()
                )
            else:
                yield '{}: {}'.format(_snake_2_camel_case(name), prop.adapt())


def _build_connections(props: T.Properties) -> t.Iterator[str]:
    from ..properties.core import PropGroup
    from ..pyside import pyside
    
    for name, prop in props.items():
        if prop is None:
            continue
        elif isinstance(prop, PropGroup):
            yield from _build_connections(prop.properties)
        else:
            for notifier_name, func in prop.bound:
                if func is None:
                    yield '{}: {}'.format(
                        _snake_2_camel_case(name),
                        _snake_2_camel_case(notifier_name)
                    )
                else:
                    # assert isinstance(notifier_name, list)
                    pyside.register(
                        lambda *args: func(),
                        name=(random_id := token_hex(8))
                    )
                    yield '{}: pyside.call("{}", {})'.format(
                        _snake_2_camel_case(name),
                        random_id,
                        list(map(_snake_2_camel_case, notifier_name))
                    )


def _build_signals(signals: T.Signals) -> t.Iterator[str]:
    for name, signal in signals.items():
        yield '{}: {}'.format(
            _snake_2_camel_case(name),
            signal.adapt()
        )


def _snake_2_camel_case(snake_case: str) -> str:
    """ snake_case to camelCase. For example, 'hello_world' -> 'helloWorld'. """
    if '.' in snake_case:
        # return '.'.join(_snake_2_camel_case(s) for s in snake_case.split('.'))
        return '.'.join(map(_snake_2_camel_case, snake_case.split('.')))
    if '_' not in snake_case:
        camel_case = snake_case
        return camel_case
    else:
        segs = snake_case.split('_')
        camel_case = segs[0] + ''.join(x.title() for x in segs[1:])
        return camel_case
