from qmlpy.widgets import Rectangle
from qmlpy.widgets import Window


def main(comp):
    comp.width = 100
    comp.height = 100
    print(':l', comp.widget_name, comp.properties)


main(Window())
main(Rectangle())
