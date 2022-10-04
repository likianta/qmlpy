import typing as t

from .prop_sheet import init_prop_sheet


class T:
    GroupName = str
    Properties = t.Dict[str, None]


class PropGroup:
    # overwrite `name` attribute in subclasses. for example see `../group_types/
    #   main.py > class Anchors > attr name`.
    name: T.GroupName
    properties: T.Properties
    
    def __init__(self):
        init_prop_sheet(self)
        
    def __repr__(self):
        return f'<{self.name}>'
    
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
