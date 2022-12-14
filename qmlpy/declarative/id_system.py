from __future__ import annotations

import typing as t
from collections import defaultdict
from dataclasses import dataclass

from .._typehint import T as T0

__all__ = ['T', 'Id', 'gen_id', 'id_gen', 'id_mgr']


class T:
    Component = T0.Component
    Componentx = t.Optional[Component]
    Id = T0.Id
    Idx = t.Optional[Id]
    IdChain = t.Dict[int, int]
    Level = int
    Token = t.Tuple[int, ...]
    #   each int is a level >= 1.
    
    GlobalIds = t.Dict[Token, Component]


@dataclass
class Id:
    token: T.Token
    
    def __str__(self) -> str:
        return '_'.join(map(str, self.token))
    
    # @property
    # def text(self) -> str:
    #     return '_'.join(map(str, self.token))
    
    @property
    def level(self) -> int:  # >= 1
        return len(self.token)
    
    @property
    def number(self) -> int:  # >= 0
        return self.token[-1]
    
    @property
    def parent(self) -> T.Idx:
        if len(self.token) > 1:
            return Id(tuple(self.token[:-1]))
        else:
            return None
    
    @property
    def last_sibling(self) -> T.Idx:
        if x := self.token[-1]:
            return Id((*self.token[:-1], x - 1))
        else:
            return None
    
    @property
    def next_sibling(self) -> 'Id':
        x = self.token[-1]
        return Id((*self.token[:-1], x + 1))


class IdGenerator:
    _level: T.Level
    _id_chain: T.IdChain
    
    def __init__(self):
        self._level = 0
        self._id_chain = defaultdict(int)
    
    def upgrade(self) -> Id:
        self._level += 1
        self._id_chain[self._level] += 1
        return self.gen_id()
    
    def downgrade(self) -> None:
        # reset children level count
        for level in range(self._level + 1, max(self._id_chain)):
            self._id_chain.pop(level)
        self._level -= 1  # go to uplevel
    
    def gen_id(self) -> Id:
        # note: the keys in self._id_chain are ordered by level sequence.
        return Id(tuple(self._id_chain.values()))


class IdFinder:
    _global_ids: T.GlobalIds
    _curr_id: T.Idx
    _root_id: T.Id
    
    def __init__(self):
        self._curr_id = None
        self._root_id = Id((1,))
        self._global_ids = {}
    
    def set_current_id(self, id_: T.Id) -> None:
        self._curr_id = id_
    
    @property
    def curr_id(self) -> T.Idx:
        return self._curr_id
    
    @property
    def root_id(self) -> T.Id:
        return self._root_id
    
    def siblings(self, id_: T.Id) -> t.List[T.Id]:
        parent_id = id_.parent
        if parent_id:
            out = []
            parent_level = parent_id.level
            parent_token = parent_id.token
            for token in self._global_ids.keys():
                if len(token) - 1 == parent_level \
                        and token[:parent_level] == parent_token:
                    out.append(Id(token))
                elif out:
                    break
            return out
        else:
            return []
    
    def get_component(self, id_: T.Idx) -> T.Componentx:
        return self._global_ids[id_.token] if id_ else None
    
    def get_children(self, id_: Id) -> t.List[T.Component]:
        out = []
        child_level = id_.level + 1
        for token, comp in self._global_ids.items():
            if len(token) == child_level and token[:id_.level] == id_.token:
                out.append(comp)
            elif out:
                break
        return out
    
    def get_all_components(self) -> t.Iterator[T.Component]:
        yield from self._global_ids.values()


class IdManager(IdFinder):
    
    def __init__(self):
        super().__init__()
    
    def register(self, id_: Id, comp: T.Component) -> None:
        self._global_ids[id_.token] = comp
    
    def walk(self) -> t.Iterator[t.Tuple[T.Token, T.Component]]:
        yield from self._global_ids.items()
    
    def finalize(self):
        pass


id_gen = IdGenerator()
gen_id = id_gen.gen_id

id_mgr = IdManager()
