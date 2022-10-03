import re
import typing as t
from collections import defaultdict
from textwrap import dedent
from textwrap import indent

from lk_utils import dumps
from lk_utils import loads

from ...common import camel_2_snake_case
from ...io import T as T0
from ...io import path

BASE_CLASS = 'P.PropSheet'


class T(T0):
    WidgetName = str  # e.g. 'Item', 'Rectangle', 'MouseArea', ...
    ParentName = WidgetName
    
    TemplateCode = str
    
    _PropName = str
    _PropType = str
    Props = t.Dict[_PropName, _PropType]
    
    WidgetSheetData1 = t.Dict[WidgetName, t.Dict[ParentName, Props]]
    WidgetSheetData2 = t.Dict[WidgetName, t.Tuple[ParentName, TemplateCode]]


def main(file_o: str = path.proj_root + '/qmlpy/widgets/widget_props.py',
         cast_safe=True):
    data_r: T.JsonData3 = loads(path.json3)
    data_w: T.WidgetSheetData1 = defaultdict(dict)
    
    # data_r 的数据结构比较复杂. 下面的代码逻辑主要基于 `io.json3.<data>.<key:qtquick>`
    # 进行观察和编写.
    
    for package, v0 in data_r.items():
        if package == '': continue
        print(':di0', package)
        
        for widget_name, v1 in v0.items():
            widget_name = 'Ps' + widget_name
            
            if v1['parent']:
                # noinspection PyTypeChecker
                parent_name = 'Ps' + v1['parent']
            else:
                parent_name = BASE_CLASS
            
            print(':i', widget_name, parent_name)
            
            props = v1['props']
            data_w[widget_name][parent_name] = props
    
    widgets_dict: T.WidgetSheetData2 = {}
    widget_tmpl: str = dedent('''
        class {WIDGET}({PARENT}):
            {PROPS}
    ''').strip()
    
    for widget_name, parent_name, raw_props in _merge_multi_parent_case(data_w):
        if raw_props:
            widgets_dict[widget_name] = (
                parent_name,
                widget_tmpl.format(
                    WIDGET=widget_name,
                    PARENT=parent_name,
                    PROPS=indent('\n'.join(
                        (f'{k} = {v}' for k, v in _generate_props(
                            raw_props, cast_safe=cast_safe
                        ))
                    ), '    ').lstrip(),
                )
            )
        else:
            widgets_dict[widget_name] = (
                parent_name,
                widget_tmpl.format(
                    WIDGET=widget_name,
                    PARENT=parent_name,
                    PROPS='pass',
                )
            )
    
    template = dedent('''
        """
        this module is auto generated by `~/blueprint/src/template_generator/
        widgets/widget_oriented_props.py`.
        please do not edit this file directly.
        
        for developer: this module shouldn't be imported by `qmlpy.properties
        .group_types.sheet` directly, although it is in the same folder.
        otherwise it will cause a circular import error.
        
        the prefix 'Ps' means 'PropSheet' derives from `qmlpy.properties
        .group_types.sheet.PropSheet`.
        the prefix 'P' means 'Property' derives from `qmlpy.properties.core
        .prop`.
        """
        from typing import cast
        
        # see `qmlpy.widgets.namespace.__qml_namespace__`
        from __qml_namespace__ import P


        {WIDGETS}
    ''')
    dumps(template.format(WIDGETS='\n\n\n'.join(
        _sort_formatted_list(widgets_dict, exclusions=(BASE_CLASS,))
    )).strip(), file_o)


def _merge_multi_parent_case(data: T.WidgetSheetData1) \
        -> t.Iterator[t.Tuple[T.WidgetName, T.ParentName, T.Props]]:
    """
    Before:
        {aaa: {bbb: {'x': 0, 'y': 0},
               ccc: {'width': 0, 'height': 0}, ...}}
    After:
        {aaa: (BASE_CLASS, {'x': 0, 'y': 0, 'width': 0, 'height': 0})}
    """
    
    def _loop(widget_name):
        if widget_name not in data:
            return
        for parent_name, props in data[widget_name].items():
            yield props
            yield from _loop(parent_name)
    
    for widget_name, v0 in data.items():
        if len(v0) == 0:
            raise ValueError(widget_name)
        elif len(v0) == 1:
            for parent_name, props in v0.items():
                yield widget_name, parent_name, props
        else:
            all_props = {}
            [all_props.update(x) for x in _loop(widget_name)]
            yield widget_name, BASE_CLASS, all_props


def _generate_props(
        props: t.Dict[str, str], cast_safe: bool
) -> t.Iterator[t.Tuple[str, str]]:
    basic_qml_types = {
        # summary:
        #   keys are qml basic types. values are `qmlpy.properties`.
        # keys:
        #   the keys are from qt documentation (see `qmlpy
        #   .properties.basic_properties.<docstring>.references`).
        #   you can also find all basic qml types in `io.json_3.<data>
        #   .<key=''>.<keys which starts with lower case character>`.
        # values:
        #   some values are tuple[python_primitive_type, custom_type], others
        #   are tuple['', custom_type].
        'bool'                : ('bool', 'Bool'),
        'color'               : ('str', 'Color'),
        'date'                : ('', 'Date'),
        'double'              : ('float', 'Double'),
        'enumeration'         : ('int', 'Enumeration'),
        #   ps: we're considering change the value to 'Enum'.
        'int'                 : ('int', 'Int'),
        'list'                : ('list', 'List'),
        'matrix4x4'           : ('', 'Matrix4x4'),
        'real'                : ('float', 'Real'),
        'string'              : ('str', 'String'),
        'url'                 : ('str', 'Url'),
        'var'                 : ('', 'Var'),
        
        # group properties
        'anchors'             : ('', 'Anchors'),
        'axis'                : ('', 'Axis'),
        'border'              : ('', 'Border'),
        'children_rect'       : ('', 'ChildrenRect'),
        'down'                : ('', 'Down'),
        'drag'                : ('', 'Drag'),
        'easing'              : ('', 'Easing'),
        'first'               : ('', 'First'),
        'font'                : ('', 'Font'),
        'font_info'           : ('', 'FontInfo'),
        'icon'                : ('', 'Icon'),
        'layer'               : ('', 'Layer'),
        'origin'              : ('', 'Origin'),
        'pinch'               : ('', 'Pinch'),
        'point'               : ('', 'Point'),
        'quaternion'          : ('', 'Quaternion'),
        'rect'                : ('', 'Rect'),
        'second'              : ('', 'Second'),
        'section'             : ('', 'Section'),
        'selected_name_filter': ('', 'SelectedNameFilter'),
        'size'                : ('', 'Size'),
        'swipe'               : ('', 'Swipe'),
        'target'              : ('', 'Target'),
        'up'                  : ('', 'Up'),
        'vector2d'            : ('', 'Vector2D'),
        'vector3d'            : ('', 'Vector3D'),
        'vector4d'            : ('', 'Vector4D'),
        'visible_area'        : ('', 'VisibleArea'),
        'word_candidate_list' : ('', 'WordCandidateList'),
        'x_axis'              : ('', 'XAxis'),
        'y_axis'              : ('', 'YAxis'),
        
        # unlisted
        'float'               : ('float', 'Number'),
    }
    
    # prop_list = []  # type: List[str]
    # prop_tmpl = '{PROP_NAME}: {PROP_TYPE}'
    
    for prop_name, prop_type in props.items():
        # adjust prop_name
        if '.' in prop_name:
            continue
        if prop_name[0].isupper():
            #   e.g. 'AlignMode'. it is an enum type.
            # TODO: convert it to all upper case.
            pass
        else:
            prop_name = camel_2_snake_case(prop_name)
            #   e.g. 'checkStateMixed' -> 'check_state_mixed'
            if prop_name in ('from', 'name', 'properties'):  # FIXME
                #   'name', 'properties' are occupied by `qmlpy.widgets.base
                #   .Component`
                prop_name += '_'
        
        # ----------------------------------------------------------------------
        
        # adjust prop_type
        prop_type = prop_type.lower()
        if '::' in prop_type:
            prop_type = prop_type.replace('::', '.')
        prop_type = re.match(r'[.\w]+', prop_type).group()
        
        if prop_type[0].isupper():  # e.g. 'Item'
            prop_type = 'cast({}, P.Delegate)'.format(prop_type)
        
        else:
            _temp_collector = defaultdict(set)  # TODO
            if prop_type == 'group':
                _temp_collector['group_props'].add((prop_name, prop_type))
                prop_type = prop_name
            
            if prop_type in basic_qml_types:
                a, b = basic_qml_types[prop_type]
                if a:
                    prop_type = 'cast({}, {})'.format(a, b)
                    #   e.g. 'cast(str, String)'
                else:
                    prop_type = b  # e.g. 'Anchors'
            else:
                prop_type = 'Property'
                # prop_type = 'cast("{}", P.Property)'.format(prop_type)
                _temp_collector['unknown_props'].add((prop_name, prop_type))
        
        if cast_safe:
            if 'cast(' in prop_type:
                prop_type = re.sub(r', (.*?)\)', r', "prop:\1")', prop_type)
                #  e.g. 'cast(str, String)' -> 'cast(str, "String")'
            else:
                prop_type = '"prop:{}"'.format(prop_type)
        
        yield prop_name, prop_type


def _sort_formatted_list(
        widgets_dict: T.WidgetSheetData2,
        exclusions: tuple = ()
) -> T.TemplateCode:
    # counter
    who_is_most_required = defaultdict(int)  # {parent_name: count, ...}
    
    def _loop(widget_name):
        if widget_name not in widgets_dict:
            print(':v3', 'this name is not in __list__', widget_name)
            return
        
        parent_name = widgets_dict[widget_name][0]
        if parent_name in exclusions:
            return
        
        who_is_most_required[parent_name] += 1
        _loop(parent_name)
    
    for widget_name in widgets_dict:
        _loop(widget_name)
    
    print(':l', "who's the most required", sorted(
        [(k, v) for k, v in who_is_most_required.items()],
        key=lambda k_v: k_v[1], reverse=True
    ))
    
    for widget_name in sorted(
            widgets_dict.keys(),
            key=lambda widget_name: who_is_most_required[widget_name],
            reverse=True
    ):
        yield widgets_dict[widget_name][1]
