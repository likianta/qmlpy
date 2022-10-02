import typing as t


class T:
    if __name__ == '__main__':
        from ...core import Id
    else:
        Id = t.Any
    Name = str
    Func = t.Callable


class Signal:
    uid: T.Id
    name: T.Name
    func: T.Func
    
    def __init__(self, uid: T.Id, name: T.Name):
        self.uid = uid
        self.name = name
    
    def connect(self, func: T.Func):
        self.func = func
    
    def emit(self, *args, **kwargs):
        self.func(*args, **kwargs)
    
    def adapt(self) -> str:
        from ...core import pyside
        func_id = str(id(self.func))
        pyside.register(self.func, name=func_id)
        return 'pyside.call("{}")'.format(func_id)
