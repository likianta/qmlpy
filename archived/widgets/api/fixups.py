from .qtquick import Window as _Window


class Window(_Window):
    
    def __getprop__(self, key):
        pass


def fixup_window_widget():
    pass
