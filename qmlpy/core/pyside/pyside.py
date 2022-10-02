import typing as t

from qtpy.QtCore import QObject
from qtpy.QtCore import Slot
from qtpy.QtQml import QJSValue

from .register import PyRegister


class T:
    PyFuncName = str
    QVal = QJSValue
    QVar = 'QVariant'


class PySide(QObject, PyRegister):
    
    @Slot(T.PyFuncName, result=T.QVar)
    @Slot(T.PyFuncName, T.QVal, result=T.QVar)
    @Slot(T.PyFuncName, T.QVal, T.QVal, result=T.QVar)
    def call(self, func_name: T.PyFuncName,
             args: t.Optional[T.QVal] = None,
             kwargs: t.Optional[T.QVal] = None):
        """ Call Python functions in QML files.
        
        See detailed docstring at `~/docs/pyside-handler-usage.md`.
        """
        func, narg = self._pyfunc_holder[func_name]  # narg: 'number of args'
        
        args = [] if args is None else (args.toVariant() or [])
        kwargs = {} if kwargs is None else (kwargs.toVariant() or {})
        
        if kwargs:
            return func(*args, **kwargs)
        elif narg == 0:
            return func()
        elif narg == -1:  # see `PyRegister._get_number_of_args.<return>`
            return func(*args)
        else:
            if isinstance(args, list) and narg > 1:
                return func(*args)
            else:  # this is a feature.
                return func(args)


pyside = PySide()
pyslot = pyside.slot
