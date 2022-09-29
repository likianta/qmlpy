class Root:
    pass


class Parent:
    pass


class This:
    _pointer = None
    
    @property
    def pointee(self):
        return self._pointer
    
    @property
    def parent(self) -> Parent:
        return parent


class Siblings:
    pass


class LastSibling:
    pass


class NextSibling:
    pass


root = Root()
parent = Parent()
this = This()
siblings = Siblings()
last_sibling = NextSibling()
next_sibling = NextSibling()
