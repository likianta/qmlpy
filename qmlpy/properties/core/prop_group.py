from .prop_sheet import init_prop_sheet
from .traits import PropGetterAndSetter


class T:
    Id = ...
    GroupName = str


class PropGroup(PropGetterAndSetter):
    uid: T.Id
    # overwrite `name` attribute in subclasses. for example see `../group_types/
    #   main.py > class Anchors > attr name`.
    name: T.GroupName
    
    def __init__(self, uid: T.Id, *_):
        PropGetterAndSetter.__init__(self)
        self.uid = uid
        init_prop_sheet(self, prefix=self.name)
    
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
        return f'{self.uid}.{self.name}'
    
    @property
    def properties(self):
        return self._properties
    
    def adapt(self) -> str:
        return self.fullname
