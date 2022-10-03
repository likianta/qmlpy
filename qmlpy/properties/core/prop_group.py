import typing as t

from .prop_sheet import init_prop_sheet
from .traits import PropGetterAndSetter
from ..._typehint import T as T0


class T:
    Id = T0.Id
    GroupName = str
    Properties = t.Dict[str, None]


class PropGroup(PropGetterAndSetter):
    id: T.Id
    # overwrite `name` attribute in subclasses. for example see `../group_types/
    #   main.py > class Anchors > attr name`.
    name: T.GroupName
    properties: T.Properties
    
    # noinspection PyShadowingBuiltins
    def __init__(self, id: T.Id, *_):
        PropGetterAndSetter.__init__(self)
        self.id = id
        init_prop_sheet(self.__class__)
    
    def kiss(self, _):
        raise Exception(
            'PropertyGroup doesnt support `kiss` method. '
            'You can only call its sub property to set values.'
        )
    
    set = kiss
    
    def bind(self, *_):
        raise Exception(
            'PropertyGroup doesnt support `bind` method. '
            'You can only call its sub property to bind values.'
        )
    
    @property
    def fullname(self) -> str:
        return f'{self.id}.{self.name}'
    
    @property
    def properties(self):
        return self._properties
    
    def adapt(self) -> str:
        return self.fullname
