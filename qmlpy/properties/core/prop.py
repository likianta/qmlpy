import typing as t

from .common_util import snake_2_camel_case
from ..._typehint import T as T0


class T:
    Id = T0.Id
    BindingArg0 = t.Union[T0.Property, t.Iterable[T0.Property]]
    BindingArg1 = t.Optional[t.Callable]
    Bound = t.List
    PropName = str


class Property:
    uid: T.Id
    name: T.PropName
    bound: T.Bound
    value: t.Any
    
    def __init__(self, uid: T.Id, name: T.PropName,
                 default_value: t.Any = None):
        """
        args:
            uid:
            name:
            default_value:
                None: no value defined, it won't be generated to QML side.
                      see processing logic in: `..builder.build_properties`.
                it is suggested that the subclasses do not override
                `default_value` in their `__init__` method.
        """
        self.uid = uid
        self.name = name
        self.bound = []
        self.value = default_value
    
    def kiss(self, arg_0: t.Any) -> None:
        self.value = arg_0
        # if isinstance(arg_0, Property):
        #     self.value = arg_0.value
        # else:
        #     self.value = arg_0
    
    set = kiss  # alias (this is more popular to use)
    
    def bind(self, arg_0: T.BindingArg0, arg_1: T.BindingArg1 = None):
        pass  # raise NotImplementedError
    
    @property
    def fullname(self) -> str:
        return f'{self.uid}.{self.name}'
    
    def adapt(self) -> str:
        """ convert python type to qml type. """
        if self.value is None:
            # return something like fullname but a little different.
            return '{}.{}'.format(
                self.uid, snake_2_camel_case(self.name)
            )
        elif isinstance(self.value, Property):
            return self.value.adapt()
        else:
            return str(self.value)
