import re
import typing as t

from ..core import Property

__all__ = [
    'AnyItem',
    'Bool',
    'Color',
    'Date',
    'Delegate',
    'Double',
    'Enumeration',
    'Int',
    'List',
    'Matrix4x4',
    'Number',
    'Real',
    'String',
    'Url',
    'Var',
]


class T:
    if __name__ == '__main__':
        from ...core import Component, Id
    else:
        Component = t.Any
        Id = t.Any
    
    Any = t.Any
    Color = str
    Date = str
    Int = int
    List = t.Union[list, tuple, set]
    Name = str
    Number = t.Union[int, float]
    String = str
    Union = t.Union
    
    Properties = t.Dict


def _getattr(self, key) -> t.Any:
    """ the primitive `getattr` method. """
    return object.__getattribute__(self, key)


class AnyItem(Property):
    _delegates: dict
    
    def __init__(self, uid: T.Id, name: T.Name):
        super().__init__(uid, name)
        self._delegates = {}
    
    def __getattr__(self, key: str):
        if key.startswith('_'):
            return _getattr(self, key)
        elif key in self.__dict__:
            return self.__dict__[key]
        elif key in self._delegates:
            return self._delegates[key]
        else:
            out = self._delegates[key] = Property(self.uid, key)
            return out


class Bool(Property):
    value: bool
    
    def adapt(self) -> str:
        return 'true' if self.value else 'false'


class Color(Property):
    """
    - svg color name. for example: 'red', 'white', 'black', etc.
    - rgb color code. for example: '#ff0000', '#ffffff', '#000000', etc.
    - argb color code. for example: '#800000ff', etc.
    - not support qt methods. for example: `Qt.rgba()`, `Qt.hsva()`, etc.
    """
    value: T.Color
    _validator = re.compile(r'^#(?:[0-9][0-9])?[0-9a-fA-F]{6}$|^\w+$')
    
    def kiss(self, arg_0: str):
        if self._validator.match(arg_0):
            self.value = arg_0
        else:
            raise ValueError(
                '{} is not a valid color value'.format(arg_0)
            )
    
    def bind(self, *args):
        raise NotImplemented("{} doesn't support bind method".format(
            self.__class__.__name__
        ))
    
    def adapt(self) -> str:
        return f'"{self.value}"'


class Date(Property):
    """
    date string. formats:
        - <YYYY>-<MM>-<DD>
        - <YYYY>-<MM>-<DD><T><hh>:<mm>
        - <YYYY>-<MM>-<DD><T><hh>:<mm>:<ss>
        - <YYYY>-<MM>-<DD><T><hh>:<mm>:<ss>.<zzz>
        - <YYYY>-<MM>-<DD><T><hh>:<mm>:<ss>.<zzz><Z>
    params:
        - <YYYY>: full year
        - <MM>: full month
        - <DD>: full day
        - <T>: time separator, it can be any character, but usually we use ' '
        - <hh>: full hour
        - <mm>: full minute
        - <ss>: full second
        - <zzz>: millisecond
        - <Z>: time zone
    note (change statement):
        - i'm not sure about the time zone format. in current version, it's not
          supported.
        - for time separator, you can only use ' '.
    """
    value: T.Date
    _validator = re.compile(
        r'[0-9]{4}-[01][0-9]-[0-3][0-9]'
        r'(?: [0-2][0-9]:[0-5][0-9]:[0-5][0-9](?:\.\d+)?)?'
    )
    
    def kiss(self, arg_0: str):
        if self._validator.match(arg_0):
            self.value = arg_0
        else:
            raise ValueError(
                '{} is not a valid date string'.format(arg_0)
            )
    
    def bind(self, *args):
        raise NotImplemented("{} doesn't support bind method".format(
            self.__class__.__name__
        ))
    
    def adapt(self) -> str:
        return f'"{self.value}"'


class Delegate(Property):
    """
    Warnings:
        This is not stable. Turn to use `AnyItem` instead.
    """
    value: T.Component
    _properties: T.Properties
    
    def __init__(self, uid: T.Id, name: T.Name,
                 delegate: T.Union[str, T.Component]):
        
        if isinstance(delegate, str):
            # find real component in `declare_qtquick.widgets.api.<globals>`
            # FIXME: we should know the exact path (for sub packages of api).
            try:
                from ...widgets import api
                delegate = getattr(api, delegate)  # type: T.Component
            except AttributeError as e:
                raise e
        
        super().__init__(uid, name, delegate())
    
    def __getattr__(self, key: str):
        if key == '_properties':
            return getattr(super(), key, ())
        elif key in self._properties:
            return getattr(self.value, key)
        else:
            return getattr(super(), key)
    
    def __setattr__(self, key: str, value):
        if key in self._properties:
            setattr(self.value, key, value)
        else:
            setattr(super(), key, value)
    
    def kiss(self, arg_0: T.Component):
        if isinstance(arg_0, Delegate):
            self.value = arg_0.value
        else:
            self.value = arg_0
        self._properties = arg_0.properties
    
    def bind(self, *args):
        raise NotImplemented("{} doesn't support bind method".format(
            self.__class__.__name__
        ))
    
    def adapt(self) -> str:
        return self.value.build(self.uid.level + 1)


class Double(Property):
    value = T.Number
    
    def adapt(self) -> str:
        return str(float(self.value))


class Enumeration(Property):
    pass


class Int(Property):
    value: T.Int
    
    def adapt(self) -> str:
        return str(int(self.value))


class List(Property):
    value: T.List
    
    def adapt(self) -> str:
        return str(list(self.value))


class Matrix4x4(Property):  # FIXME: not implemented
    pass


class Number(Property):
    value: T.Number


class Real(Number):
    pass


class String(Property):
    value: T.String
    
    def adapt(self) -> str:
        return f'"{self.value}"'


class Url(String):
    pass


class Var(Property):
    value: T.Any
