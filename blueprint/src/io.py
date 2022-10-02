from __future__ import annotations

import typing as t

from lk_utils import relpath

__all__ = ['T', 'path']


class path:  # noqa
    proj_root = relpath('../..')
    blueprint = f'{proj_root}/blueprint'
    resources = f'{proj_root}/blueprint/resources'
    qt_source = None  # TODO
    #   see `../readme.md > requirements > qt documents`.
    
    html1 = f'{resources}/qtdoc/1_all_qml_modules.html'
    html2 = f'{resources}/qtdoc/2_all_qml_types.html'
    
    json1 = f'{resources}/qtdoc_compiled/1_all_qml_modules.json'
    json2 = f'{resources}/qtdoc_compiled/2_all_qml_types.json'
    json3 = f'{resources}/qtdoc_compiled/3_all_qml_widgets.json'
    json4 = f'{resources}/qtdoc_compiled/4_all_qmlpy_widgets.json'
    
    temp1 = f'{resources}/widgets_template/__base__.txt'
    temp2 = f'{resources}/widgets_template/__init__.txt'
    temp3 = f'{resources}/widgets_template/__list__.txt'
    temp4 = f'{resources}/widgets_template/readme.md'
    temp5 = f'{resources}/widgets_template/api_init.txt'
    
    prop1 = f'{resources}/properties/basic_types.json'
    prop2 = f'{resources}/properties/group_types.json'
    
    @property
    def step1(self) -> tuple[str, str]:
        return self.html1, self.json1
    
    @property
    def step2(self) -> tuple[str, str]:
        return self.html2, self.json2
    
    @property
    def step3(self) -> tuple[str, str]:
        return self.json2, self.json3
    
    @property
    def step4(self) -> tuple[str, str]:
        return self.json3, self.json4


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
    
    JsonData3 = t.Dict[str, t.Dict[
        str, JsonData3WidgetInfo := t.TypedDict(
            'JsonData3WidgetInfo', {
                'parent': t.List[str],
                'props' : t.Dict[str, str],
            }
        )
    ]]
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
                    'parent': 'Item',  # usually 'Item' can be found in the
                    #   same module, but sometimes it may be in another module.
                    #   see `./template_generator/widgets/widgets_api.py > def
                    #   _fix_missing_parents()`.
                    'props': {
                        'antialiasing': 'bool',
                        'border': 'group', ...
                    }
                }, ...
            }, ...
        }
    '''
