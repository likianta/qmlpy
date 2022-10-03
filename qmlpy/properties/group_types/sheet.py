"""
this is hand-made module, based on the infomation of `~/blueprint/run.py : def
list_all_group_properties`.
"""
from typing import Union
from typing import cast

from ..basic_types import *
from ..core import PropSheet
#   note: the PropSheet has nothing defined. we use it as the ancestor of all
#   group types, to make sure the recursive class-base-finder works correctly.
from ..core import Property

# appendix types
num = Union[int, float]
enum = Union[str, int]

__all__ = [
    'PsAnchors',
    'PsAxis',
    'PsBorder',
    'PsChildrenRect',
    'PsDown',
    'PsDrag',
    'PsEasing',
    'PsFirst',
    'PsFont',
    'PsFontInfo',
    'PsIcon',
    'PsLayer',
    'PsOrigin',
    'PsPinch',
    'PsPoint',
    'PsQuaternion',
    'PsRect',
    'PsSecond',
    'PsSection',
    'PsSelectedNameFilter',
    'PsSize',
    'PsSwipe',
    'PsTarget',
    'PsUp',
    'PsVector2D',
    'PsVector3D',
    'PsVector4D',
    'PsVisibleArea',
    'PsWordCandidateList',
    'PsXAxis',
    'PsYAxis',
]


# ------------------------------------------------------------------------------
# Found in 'All QML Basic Types'

class PsFont(PropSheet):
    """
    Index:
        Qt 6 > Qt Quick > QML Types > font QML Basic Type
    """
    bold = cast(bool, Bool)
    capitalization = cast(enum, Enumeration)
    family = cast(str, String)
    hinting_preference = cast(enum, Enumeration)
    italic = cast(bool, Bool)
    kerning = cast(bool, Bool)
    letter_spacing = cast(float, Number)
    overline = cast(bool, Bool)
    pixel_size = cast(int, Number)
    point_size = cast(float, Number)
    prefer_shaping = cast(bool, Bool)
    strikeout = cast(bool, Bool)
    style_name = cast(str, String)
    underline = cast(bool, Bool)
    weight = cast(enum, Enumeration)
    word_spacing = cast(float, Number)


class PsPoint(PropSheet):
    x = cast(num, Number)
    y = cast(num, Number)


class PsQuaternion(PropSheet):
    scalar = cast(num, Number)
    x = cast(num, Number)
    y = cast(num, Number)
    z = cast(num, Number)


class PsRect(PropSheet):
    height = cast(num, Number)
    width = cast(num, Number)
    x = cast(num, Number)
    y = cast(num, Number)


class PsSize(PropSheet):
    height = cast(num, Number)
    width = cast(num, Number)


class PsVector2D(PropSheet):
    x = cast(num, Number)
    y = cast(num, Number)


class PsVector3D(PropSheet):
    x = cast(num, Number)
    y = cast(num, Number)
    z = cast(num, Number)


class PsVector4D(PropSheet):
    w = cast(num, Number)
    x = cast(num, Number)
    y = cast(num, Number)
    z = cast(num, Number)


# ------------------------------------------------------------------------------
# Found in Qt Doc (All QML Types)

''' All 'group' Types Found in Qt Doc

- anchors
- axis
- border
- children_rect
- down
- drag
- easing
- first
- icon
- origin
- pinch
- second
- section
- selected_name_filter
- swipe
- target_property
- up
- visible_area
- word_candidate_list
- x_axis
- y_axis

You can use `blueprint/src/sidework/list_all_group_properties.py` to view their
detailed attributes.
'''


class PsAnchors(PropSheet):
    align_when_centered = cast(bool, Bool)
    baseline: Property
    baseline_offset = cast(num, Number)
    bottom: Property
    bottom_margin = cast(num, Number)
    center_in: Property
    fill: Property
    horizontal_center: Property
    horizontal_center_offset = cast(num, Number)
    left: Property
    left_margin = cast(num, Number)
    margins = cast(num, Number)
    right: Property
    right_margin = cast(num, Number)
    top_margin = cast(num, Number)
    top: Property
    vertical_center: Property
    vertical_center_offset = cast(num, Number)


class PsAxis(PropSheet):
    x = cast(num, Number)
    y = cast(num, Number)
    z = cast(num, Number)


class PsBorder(PropSheet):
    bottom = cast(num, Number)
    color = cast(str, Color)
    left = cast(num, Number)
    right = cast(num, Number)
    top = cast(num, Number)
    width = cast(num, Number)


class PsChildrenRect(PropSheet):
    height = cast(num, Number)
    width = cast(num, Number)
    x = cast(num, Number)
    y = cast(num, Number)


class PsDown(PropSheet):
    hovered = cast(bool, Bool)
    implicit_indicator_height = cast(num, Number)
    implicit_indicator_width = cast(num, Number)
    indicator: AnyItem
    pressed = cast(bool, Bool)


class PsDrag(PropSheet):
    active = cast(bool, Bool)
    axis = cast(enum, Enumeration)
    filter_children = cast(bool, Bool)
    maximum_x = cast(num, Number)
    maximum_y = cast(num, Number)
    minimum_x = cast(num, Number)
    minimum_y = cast(num, Number)
    smoothed = cast(bool, Bool)
    source: AnyItem
    target: AnyItem
    threshold = cast(num, Number)
    x = cast(num, Number)
    y = cast(num, Number)


class PsEasing(PropSheet):
    amplitude = cast(num, Number)
    bezier_curve = cast(list, List)
    overshoot = cast(num, Number)
    period = cast(num, Number)
    type = cast(enum, Enumeration)


class PsFirst(PropSheet):
    handle: AnyItem
    hovered = cast(bool, Bool)
    implicit_handle_height = cast(num, Number)
    implicit_handle_width = cast(num, Number)
    position = cast(num, Number)
    pressed = cast(bool, Bool)
    value = cast(num, Number)
    visual_position = cast(num, Number)


class PsFontInfo(PropSheet):
    bold = cast(bool, Bool)
    family = cast(str, String)
    italic = cast(bool, Bool)
    pixel_size = cast(str, String)
    point_size = cast(num, Number)
    style_name = cast(str, String)
    weight = cast(int, Int)


class PsIcon(PropSheet):
    cache = cast(bool, Bool)
    color = cast(str, Color)
    height = cast(num, Number)
    mask = cast(bool, Bool)
    name_ = cast(str, String)
    source = cast(str, Url)
    width = cast(num, Number)


class PsLayer(PropSheet):
    effect: AnyItem
    enabled = cast(bool, Bool)
    format = cast(enum, Enumeration)
    mipmap = cast(bool, Bool)
    sampler_name = cast(str, String)
    samples = cast(enum, Enumeration)
    smooth = cast(bool, Bool)
    source_rect: PsRect
    texture_mirroring = cast(enum, Enumeration)
    texture_size: PsSize
    wrap_mode = cast(enum, Enumeration)


class PsOrigin(PropSheet):
    x = cast(num, Number)
    y = cast(num, Number)


class PsPinch(PropSheet):
    active = cast(bool, Bool)
    drag_axis = cast(enum, Enumeration)
    maximum_rotation = cast(num, Number)
    maximum_scale = cast(num, Number)
    maximum_x = cast(num, Number)
    maximum_y = cast(num, Number)
    minimum_rotation = cast(num, Number)
    minimum_scale = cast(num, Number)
    minimum_x = cast(num, Number)
    minimum_y = cast(num, Number)
    target: AnyItem


class PsSecond(PropSheet):
    handle: AnyItem
    hovered = cast(bool, Bool)
    implicit_handle_height = cast(num, Number)
    implicit_handle_width = cast(num, Number)
    position = cast(num, Number)
    pressed = cast(bool, Bool)
    value = cast(num, Number)
    visual_position = cast(num, Number)


class PsSection(PropSheet):
    criteria = cast(enum, Enumeration)
    delegate: AnyItem
    label_positioning = cast(enum, Enumeration)
    property = cast(str, String)


class PsSelectedNameFilter(PropSheet):
    extensions = cast(list, List)
    index = cast(int, Int)
    name_ = cast(str, String)


class PsSwipe(PropSheet):
    behind: AnyItem
    behind_item: AnyItem
    complete = cast(bool, Bool)
    enabled = cast(bool, Bool)
    left: AnyItem
    left_item: AnyItem
    position = cast(num, Number)
    right: AnyItem
    right_item: AnyItem
    # noinspection PyUnresolvedReferences
    transition: AnyItem


class PsTarget(PropSheet):
    name_ = cast(str, String)
    object: AnyItem


class PsUp(PropSheet):
    hovered = cast(bool, Bool)
    implicit_indicator_height = cast(num, Number)
    implicit_indicator_width = cast(num, Number)
    indicator: AnyItem
    pressed = cast(bool, Bool)


class PsVisibleArea(PropSheet):
    height_ratio = cast(num, Number)
    width_ratio = cast(num, Number)
    x_position = cast(num, Number)
    y_position = cast(num, Number)


class PsWordCandidateList(PropSheet):
    always_visible = cast(bool, Bool)
    auto_hide_delay = cast(int, Int)


class PsXAxis(PropSheet):
    enabled = cast(bool, Bool)
    maximum = cast(num, Number)
    minimum = cast(num, Number)


class PsYAxis(PropSheet):
    enabled = cast(bool, Bool)
    maximum = cast(num, Number)
    minimum = cast(num, Number)
