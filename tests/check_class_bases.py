from qmlpy.properties.core import PropSheet
from qmlpy.widgets import Window


def check_bases(cls):
    temp = cls
    max_tries = 10
    while temp.__bases__ and max_tries > 0:
        print(temp.__bases__)
        temp = temp.__bases__[-1]
        print(temp, issubclass(temp, PropSheet))
        max_tries -= 1


print(Window.__bases__)
check_bases(Window)
