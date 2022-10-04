from __future__ import annotations

import typing as t

from .compositor import build_component
from .declarative import Id
from .declarative import ctx_mgr


class T:
    Level = int  # 1, 2, 3, ... see also `.declarative.id_system.Id.level`


class Component:
    id: Id
    signals = {}  # TEST
    properties: dict
    
    def __enter__(self) -> t.Self:
        self.id = ctx_mgr.enter(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        ctx_mgr.leave()
    
    @property
    def level(self) -> T.Level:
        return self.id.level
    
    @property
    def widget_name(self):
        return self.__class__.__name__
    
    def build(self) -> str:
        return build_component(self)
