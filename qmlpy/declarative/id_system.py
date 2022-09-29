from __future__ import annotations

import typing as t
from collections import defaultdict
from dataclasses import dataclass


class T:
    Component = ...
    Level = int
    IdChain = t.Dict[int, int]
    Token = t.Tuple[int, ...]


@dataclass
class Id:
    token: T.Token
    
    def __str__(self) -> str:
        return self.text
    
    @property
    def text(self) -> str:
        return '_'.join(map(str, self.token))
    
    @property
    def level(self) -> int:  # >= 1
        return len(self.token)
    
    @property
    def number(self) -> int:  # >= 0
        return self.token[-1]
    
    @property
    def parent(self) -> t.Optional['Id']:
        if len(self.token) > 1:
            return Id(tuple(self.token[:-1]))
        else:
            return None
    
    @property
    def last_sibling(self) -> t.Optional['Id']:
        if x := self.token[-1]:
            return Id((*self.token[:-1], x - 1))
        else:
            return None
    
    @property
    def next_sibling(self) -> 'Id':
        x = self.token[-1]
        return Id((*self.token[:-1], x + 1))


class IdGenerator:
    level: T.Level
    _id_chain: T.IdChain
    
    def __init__(self):
        self.level = 0
        self._id_chain = defaultdict(int)
    
    def upgrade(self) -> T.Level:
        self.level += 1
        self._id_chain[self.level] += 1
        return self.level
    
    def downgrade(self) -> T.Level:
        # reset children level count
        for level in range(self.level + 1, max(self._id_chain)):
            self._id_chain.pop(level)
        self.level -= 1  # go to uplevel
        return self.level
    
    def gen_id(self) -> Id:
        # note: the keys in self._id_chain are ordered by level sequence.
        return Id(tuple(self._id_chain.values()))


class IdManager:
    _tile_struct: dict
    _relations: dict
    
    def __init__(self):
        self._tile_struct = {}
    
    def set(self, qid: T.Qid, comp: T.Component):
        self._tile_struct[qid] = comp
    
    def finalized(self):
        self._relations = defaultdict(list)
        for qid, comp in self._tile_struct.items():
            # assert '_' in qid
            parent_qid = qid.rsplit('_', 1)[0]
            self._relations[parent_qid].append(comp)
    
    def get_component(self, qid: T.Qid) -> T.Component:
        return self._tile_struct[qid]
    
    def get_children(self, qid: T.Qid) -> T.QidList:
        return self._relations.get(qid, [])
    
    def get_all_components(self):
        for qid, comp in self._tile_struct.items():
            yield qid, comp


id_gen = IdGenerator()
gen_id = id_gen.gen_id

id_mgr = IdManager()
