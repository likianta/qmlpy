from .id_system import T
from .id_system import id_gen
from .id_system import id_mgr

__all__ = ['ctx_mgr']


class ContextManager:
    
    @staticmethod
    def enter(comp: T.Component) -> None:
        id_ = id_gen.upgrade()
        id_mgr.register(id_, comp)
    
    @staticmethod
    def leave() -> None:
        id_gen.downgrade()


ctx_mgr = ContextManager()
