import re
import typing as t

from . import proxy
from ..._typehint import T as T0


class T:
    Enums = t.Dict[str, t.Union[int, float, bool, str]]
    Props = t.Dict[str, t.Union[T0.Property, T0.PropGroup]]
    Signals = t.Dict[str, t.Callable]


def _setattr(self, name, value):
    object.__setattr__(self, name, value)


def _getattr(self, name):
    return object.__getattribute__(self, name)


# ------------------------------------------------------------------------------

class ConstantEnumeration:
    _enumerations: T.Enums
    
    def __init__(self):
        self._enumerations = {}
    
    def __getattr__(self, key: str):
        if key == '_enumerations':
            try:
                return _getattr(self, '_enumerations')
            except AttributeError:
                return ()
        elif key.startswith('_'):
            return _getattr(self, key)
        
        if key in self._enumerations:
            return self.__getenum__(key)
        else:
            return self.__getattribute__(key)
    
    def __setattr__(self, key: str, value):
        if key == '_enumerations':
            if self._enumerations:
                raise AttributeError('ConstantEnumeration is immutable!')
            else:
                _setattr(self, '_enumerations', value)
                return
        elif key.startswith('_'):
            _setattr(self, key, value)
            return
        
        if key in self._enumerations:
            self.__setenum__(key, value)
        else:
            _setattr(self, key, value)
    
    def __getenum__(self, key: str):
        return self._enumerations[key]
    
    def __setenum__(self, *_):
        raise AttributeError('ConstantEnumeration is immutable!')


class PropGetterAndSetter:
    _properties: T.Props
    
    def __init__(self):
        # the subclass should update `properties` in its `__init__` method.
        self._properties = {}
    
    def __getattr__(self, key: str):
        if key == '_properties':
            try:
                return _getattr(self, '_properties')
            except AttributeError:
                return ()
        elif key.startswith('_'):
            return _getattr(self, key)
        
        if key in self._properties:
            return self.__getprop__(key)
        else:
            return self.__getattribute__(key)
    
    def __setattr__(self, key: str, value):
        if key == '_properties' or key.startswith('_'):
            _setattr(self, key, value)
            return
        
        if key in self._properties:
            self.__setprop__(key, value)
        else:
            _setattr(self, key, value)
    
    def __getprop__(self, key):
        return proxy.getprop(
            self, key, self._properties[key]
        )
    
    def __setprop__(self, key, value):
        return proxy.setprop(
            self, key, value,
            lambda key, value: self._properties[key].set(value)
        )


class SignalHandler:
    _signals: T.Signals
    _signal_pattern = re.compile(r'^on_\w+ed$')
    
    def __init__(self):
        self._signals = {}
    
    def _is_signal(self, item: str):
        return bool(self._signal_pattern.match(item))
    
    def _signal_factory(self, key):
        raise NotImplementedError
    
    def __getattr__(self, key: str):
        if key == '_signals':
            try:
                return _getattr(self, '_signals')
            except AttributeError:
                return ()
        elif key.startswith('_'):
            return _getattr(self, key)
        
        if key in self._signals:
            return self.__getsignal__(key)
        elif self._is_signal(key):
            signal = self._signals[key] = self._signal_factory(key)
            return signal
        else:
            return self.__getattribute__(key)
    
    def __setattr__(self, key: str, value):
        if key == '_signals' or key.startswith('_'):
            _setattr(self, key, value)
            return
        
        if key in self._signals:
            self.__setsignal__(key, value)
        else:
            _setattr(self, key, value)
    
    def __getsignal__(self, key: str):
        return self._signals[key]
    
    def __setsignal__(self, key, value):
        raise AttributeError('Signal is immutable!')
