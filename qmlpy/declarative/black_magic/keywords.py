"""
extended keywords for dynamic references.
"""
import typing as t

from ..id_system import T as T0
from ..id_system import id_mgr


class T(T0):
    Node = 'Node'
    Nodex = t.Optional[Node]
    FixedNode = 'FixedNode'
    FixedNodex = t.Optional[FixedNode]


class FixedNode:
    def __init__(self, id_: T.Idx):
        self._id = id_
    
    @property
    def id(self) -> T.Idx:
        raise self._id
    
    @property
    def parent(self) -> T.FixedNodex:
        return FixedNode(self._id.parent) if self._id else None
    
    @property
    def pointee(self) -> T.Componentx:
        return id_mgr.get_component(self._id)


class Node:
    
    @property
    def id(self) -> T.Idx:
        raise NotImplementedError
    
    @property
    def pointee(self) -> T.Componentx:
        return id_mgr.get_component(self.id)


# -----------------------------------------------------------------------------

class Root(FixedNode):
    def __init__(self):
        super().__init__(id_mgr.root_id)
    
    @property
    def parent(self) -> None:
        return None


class Parent(Node):
    @property
    def id(self) -> T.Idx:
        return id_mgr.curr_id.parent
    
    @property
    def parent(self) -> T.FixedNodex:
        return FixedNode(self.id.parent) if self.id else None


class This(Node):
    
    @property
    def id(self) -> T.Idx:
        return id_mgr.curr_id
    
    @property
    def parent(self) -> T.FixedNodex:
        return FixedNode(self.id.parent) if self.id else None
    
    @property
    def last_sibling(self) -> 'LastSibling':
        return last_sibling
    
    @property
    def next_sibling(self) -> 'NextSibling':
        return next_sibling
    
    # @property
    # def siblings(self) -> t.List[T.FixedNode]:
    #     pass


class LastSibling(Node):
    
    @property
    def id(self) -> T.Idx:
        return id_mgr.curr_id.last_sibling
    
    @property
    def last_sibling(self) -> T.FixedNodex:
        return FixedNode(self.id.last_sibling) if self.id else None
    
    @property
    def next_sibling(self) -> This:
        return this


class NextSibling(Node):
    
    @property
    def id(self) -> T.Id:
        return id_mgr.curr_id.next_sibling
    
    @property
    def last_sibling(self) -> This:
        return this
    
    @property
    def next_sibling(self) -> T.FixedNode:
        return FixedNode(self.id.next_sibling)


root = Root()
parent = Parent()
this = This()
last_sibling = LastSibling()
next_sibling = NextSibling()
