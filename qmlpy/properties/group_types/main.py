from .sheet import *
from ..core import PropGroup
from ..core import proxy

__all__ = [
    'Anchors',
    'Axis',
    'Border',
    'ChildrenRect',
    'Down',
    'Drag',
    'Easing',
    'First',
    'Font',
    'FontInfo',
    'Icon',
    'Layer',
    'Origin',
    'Pinch',
    'Point',
    'Quaternion',
    'Rect',
    'Second',
    'Section',
    'SelectedNameFilter',
    'Size',
    'Swipe',
    'Target',
    'Up',
    'Vector2D',
    'Vector3D',
    'Vector4D',
    'VisibleArea',
    'WordCandidateList',
    'XAxis',
    'YAxis',
]


class Anchors(PropGroup, PsAnchors):
    name = 'anchors'
    
    # ref: declare_qtquick.control.traits.PropGetterAndSetter
    #      .__getprop__,.__setprop__
    
    def __getprop__(self, key: str):
        if key == 'center_in' or key == 'fill':
            raise AttributeError('You cannot access this property from getter, '
                                 'this is a write-only property.', key)
        elif key == 'horizontal_center' or key == 'vertical_center':
            return proxy.getprop(self, key, self.fullname)  # -> str
        elif key == 'margins' or key.endswith('_margin'):  # -> int or float
            return proxy.getprop(self, key, self._properties[key].value)
        else:  # left, top, right, bottom
            return proxy.getprop(self, key, f'{self.fullname}.{key}')
    
    def __setprop__(self, key, value):
        if key == 'center_in' or key == 'fill':
            from ...widgets.api.qtquick import Window
            if isinstance(value, str):
                # # self._properties[key].set(value)
                proxy.setprop(
                    self, key, value,
                    lambda key, value: self._properties[key].set(value)
                )
            elif isinstance(value, Window):
                # # self._properties[key].set(value.content_item)
                proxy.setprop(
                    self, key, value,
                    lambda key, value: self._properties[key].set(
                        value.content_item)
                )
            else:
                # # self._properties[key].set(value.qid)
                proxy.setprop(
                    self, key, value,
                    lambda key, value: self._properties[key].set(value.qid)
                )
        elif key == 'margins' or key.endswith('_margin'):
            # assert isinstance(value, (int, float))
            # # self._properties[key].set(value)
            proxy.setprop(
                self, key, value,
                lambda key, value: self._properties[key].set(value)
            )
        elif key == 'horizontal_center' or key == 'vertical_center':
            # assert value == key
            # # self._properties[key].set(value)
            proxy.setprop(
                self, key, value,
                lambda key, value: self._properties[key].set(value)
            )
        else:  # left, top, right, bottom
            # # self._properties[key].set(value)
            proxy.setprop(
                self, key, value,
                lambda key, value: self._properties[key].set(value)
            )


class Axis(PropGroup, PsAxis):
    name = 'axis'


class Border(PropGroup, PsBorder):
    name = 'border'


class ChildrenRect(PropGroup, PsChildrenRect):
    name = 'children_rect'


class Down(PropGroup, PsDown):
    name = 'down'


class Drag(PropGroup, PsDrag):
    name = 'drag'


class Easing(PropGroup, PsEasing):
    name = 'easing'


class First(PropGroup, PsFirst):
    name = 'first'


class Font(PropGroup, PsFont):
    name = 'font'


class FontInfo(PropGroup, PsFontInfo):
    name = 'fontInfo'


class Icon(PropGroup, PsIcon):
    name = 'icon'


class Layer(PropGroup, PsLayer):
    name = 'layer'


class Origin(PropGroup, PsOrigin):
    name = 'origin'


class Pinch(PropGroup, PsPinch):
    name = 'pinch'


class Point(PropGroup, PsPoint):
    name = 'point'


class Quaternion(PropGroup, PsQuaternion):
    name = 'quaternion'


class Rect(PropGroup, PsRect):
    name = 'rect'


class Second(PropGroup, PsSecond):
    name = 'second'


class Section(PropGroup, PsSection):
    name = 'section'


class SelectedNameFilter(PropGroup, PsSelectedNameFilter):
    name = 'selected_name_filter'


class Size(PropGroup, PsSize):
    name = 'size'


class Swipe(PropGroup, PsSwipe):
    name = 'swipe'


class Target(PropGroup, PsTarget):
    name = 'target'


class Up(PropGroup, PsUp):
    name = 'up'


class Vector2D(PropGroup, PsVector2D):
    name = 'vector2d'


class Vector3D(PropGroup, PsVector3D):
    name = 'vector3d'


class Vector4D(PropGroup, PsVector4D):
    name = 'vector4d'


class VisibleArea(PropGroup, PsVisibleArea):
    name = 'visible_area'


class WordCandidateList(PropGroup, PsWordCandidateList):
    name = 'word_candidate_list'


class XAxis(PropGroup, PsXAxis):
    name = 'x_axis'


class YAxis(PropGroup, PsYAxis):
    name = 'y_axis'
