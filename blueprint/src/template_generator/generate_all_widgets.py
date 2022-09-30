"""
References:
    blueprint/resources/widgets_template
"""
import shutil
from collections import namedtuple
from os import mkdir
from os import path as ospath
from textwrap import dedent

from lk_utils import dumps
from lk_utils import loads

from blueprint.src import io
from blueprint.src.common import sort_formatted_list
from blueprint.src.typehint import *


def main(widgets_dir=io.widgets_dir):
    """
    Input:
        io.json_3 (this is generated by `..qml_modules_indexing.no3_all_qml
        _widgets`.)
        io.module_1, io.module_2, io.module_3.
    
    Output:
        widgets_dir (the default is `declare_qtquick.widgets.api.*`)
    """
    data_r = loads(io.json_3)  # type: TJson3Data
    
    # data_r 的数据结构比较复杂. 下面的代码逻辑主要基于 `io.json_4.<data>.<key
    # :qtquick>` 进行观察和编写.
    
    print('creating dirs', ':d')
    _create_dirs(widgets_dir, data_r.keys())
    
    BILTuple = namedtuple('BIL', ('base', 'init', 'list'))
    tmpl_files = BILTuple(
        f'{io.resources_dir}/widgets_template/__base__.txt',
        f'{io.resources_dir}/widgets_template/__init__.txt',
        f'{io.resources_dir}/widgets_template/__list__.txt',
    )
    tmpl_data = BILTuple(*map(loads, tmpl_files))
    
    for package, v0 in data_r.items():
        if package == '': continue
        print(package, ':di')
        
        target_dir = f'{widgets_dir}/{package.replace(".", "/").lower()}'
        target_files = BILTuple(
            f'{target_dir}/__base__.py',
            f'{target_dir}/__init__.py',
            f'{target_dir}/__list__.py',
        )
        assert not ospath.exists(target_files.init)
        
        # generate target files (__base__, __init__, __list__).
        _generate_base(tmpl_files.base, target_files.base)
        _generate_init(tmpl_data.init, target_files.init, package=package)
        _generate_list(tmpl_data.list, target_files.list, data=v0)
    
    # put readme and __init__ files in api root dir.
    shutil.copyfile(io.readme, f'{widgets_dir}/readme.md')
    shutil.copyfile(io.api_init, f'{widgets_dir}/__init__.py')


# ------------------------------------------------------------------------------

def _create_dirs(widgets_dir, packages):
    dirs_ = set()
    
    for pkg in packages:
        if pkg == '':
            continue
        else:
            pkg = pkg.lower()
        
        tmp = widgets_dir
        for node in pkg.split('.'):
            tmp += '/' + node
            dirs_.add(tmp)
    
    for d in sorted(dirs_):
        print(':i', ospath.relpath(d, widgets_dir))
        if not ospath.exists(d):
            mkdir(d)


def _generate_base(file_i: TPath, file_o: TPath):
    # there is no placeholders in file_i. we just copy file_i to file_o.
    shutil.copyfile(file_i, file_o)


def _generate_init(tmpl_i: str, file_o: TPath, package):
    # tmpl: 'template'
    # kwargs: {'package': <str>}
    dumps(
        tmpl_i.format(QMLTYPE=package).strip(),
        file_o
    )


def _generate_list(tmpl_i: str, file_o: TPath, data: TWidgetData):
    # tmpl: 'template'
    # kwargs: {
    #   'data': {  # type: TWidgetData
    #       <str widget_name>: {
    #           'parent': (<str parent_package>,
    #                      <str parent_name>),
    #           'props': {
    #               <str prop_name>: <str prop_type>,
    #               ...
    #           }
    #       }
    #   }
    # }
    
    base_component = 'C'
    # # base_component = 'Component'
    
    widgets_dict = {}  # type: TWidgetSheetData2
    widget_tmpl = dedent('''
        class {WIDGET}({PARENT}, {PROP_SHEET}):
            pass
    ''').strip()
    
    for widget_name, v0 in data.items():
        parent_name = v0['parent'] or base_component
        print(widget_name, parent_name, ':i')
        
        widgets_dict[widget_name] = (
            parent_name,
            widget_tmpl.format(
                WIDGET=widget_name,
                PARENT=parent_name,
                PROP_SHEET=f'W.Ps{widget_name}'
            )
        )
    
    dumps(tmpl_i.format(WIDGETS='\n\n\n'.join(
        sort_formatted_list(widgets_dict, (base_component,))
    )).strip(), file_o)


if __name__ == '__main__':
    # mkdir('../../../tests/api')
    # main('../../../tests/api')
    mkdir(io.widgets_dir)
    main(io.widgets_dir)
