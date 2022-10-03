from .id_system import T
from .id_system import id_gen
from .id_system import id_mgr

__all__ = ['ctx_mgr']


class ContextManager:
    
    @staticmethod
    def enter(comp: T.Component) -> T.Id:
        id_ = id_gen.upgrade()
        id_mgr.register(id_, comp)
        id_mgr.set_current_id(id_)
        return id_
    
    @staticmethod
    def leave() -> None:
        id_gen.downgrade()
        id_mgr.set_current_id(id_mgr.curr_id.parent)


ctx_mgr = ContextManager()
