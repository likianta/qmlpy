from __future__ import annotations

import typing as t

from lk_utils import relpath


class path:  # noqa
    proj_root = relpath('../..')
    blueprint = f'{proj_root}/blueprint'
    resources = f'{blueprint}/blueprint/resources'
    qt_source = None  # TODO: set your own qt source path
    
    html_1 = f'{resources}/qtdoc/1_all_qml_modules.html'
    html_2 = f'{resources}/qtdoc/2_all_qml_types.html'
    
    json_1 = f'{resources}/qtdoc_compiled/1_all_qml_modules.json'
    json_2 = f'{resources}/qtdoc_compiled/2_all_qml_types.json'
    json_3 = f'{resources}/qtdoc_compiled/3_all_qml_widgets.json'
    json_4 = f'{resources}/qtdoc_compiled/4_all_qmlpy_widgets.json'
    
    temp_1 = f'{resources}/widgets_template/__base__.py'
    temp_2 = f'{resources}/widgets_template/__init__.py'
    temp_3 = f'{resources}/widgets_template/__list__.py'
    temp_4 = f'{resources}/widgets_template/readme.md'
    temp_5 = f'{resources}/widgets_template/api_init.py'
    
    prop_1 = f'{resources}/properties/basic_types.json'
    prop_2 = f'{resources}/properties/group_types.json'
    
    @property
    def step_1(self) -> tuple[str, str]:
        return self.html_1, self.json_1
    
    @property
    def step_2(self) -> tuple[str, str]:
        return self.html_2, self.json_2
    
    @property
    def step_3(self) -> tuple[str, str]:
        return self.json_2, self.json_3
    
    @property
    def step_4(self) -> tuple[str, str]:
        return self.json_3, self.json_4


class T:
    JsonData1 = t.TypedDict('JsonData1', {
        'module_group': t.Dict[str, str],
        'module': t.Dict[str, str],
    })
    ''' str#1. module name in all lower case, e.g. 'qtquick'.
        str#2: module name, e.g. 'QtQuick'.
        str#3: sub module name in all lower case, e.g. 'qtquick-controls'.
        str#4: sub module name, e.g. 'QtQuick.Controls'.
    '''
    
    JsonData2 = t.Dict[str, t.Dict[str, str]]
    ''' str#1: module name in PascalCase. e.g. 'QtQuick'
        str#2: qmltype name in PascalCase. e.g. 'QtQuick.Layouts'
        str#3: a relative path to a html file. the path starts from `qtdoc_dir`.
            e.g. 'qtcharts/qml-qtcharts-abstractaxis.html'.
    '''
    
    JsonData3 = t.Dict[str, t.Dict[str, t.TypedDict('WidgetInfo', {
        'parent': t.List[str],
        'props' : t.Dict[str, str],
    })]]
    ''' e.g. {
            'QtQuick': {
                'Rectangle': {
                    'parent': ['QtQuick', 'Item'],
                    'props': {
                        'border': 'group',
                        'border.color': 'color', ...
                    }
                }, ...
            }, ...
        }
    '''
    
    JsonData4 = t.Dict[str, t.Dict[str, t.TypedDict('WidgetInfo', {
        'parent': str,
        'props' : t.Dict[str, str],
    })]]
    ''' e.g. {
            'qtquick.controls': {
                'Button': {
                    'parent': 'AbstractButton',
                    'props': {
                        'flat': 'bool',
                        'highlighted': 'bool', ...
                    }
                }, ...
            },
            'qtquick': {
                'Rectangle': {
                    'parent': 'Item',
                    'props': {
                        'antialiasing': 'bool',
                        'border': 'group', ...
                    }
                }, ...
            }, ...
        }
    '''
