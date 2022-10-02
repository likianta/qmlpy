import shutil
from collections import namedtuple
from os import mkdir
from os import path as ospath
from textwrap import dedent

from lk_utils import dumps
from lk_utils import loads

from .widget_oriented_props import T as T1
from .widget_oriented_props import _sort_formatted_list
from ...io import T as T0
from ...io import path


class T(T0, T1):
    pass


def main(widgets_dir=path.proj_root + '/qmlpy/widgets'):
    data_r: T.JsonData3 = loads(path.json3)
    
    # data_r 的数据结构比较复杂. 下面的代码逻辑主要基于 `io.json3.<data>.<key
    # :qtquick>` 进行观察和编写.
    
    print('creating dirs', ':d')
    _create_dirs(widgets_dir, data_r.keys())
    
    BaseInitList = namedtuple('BaseInitList', ('base', 'init', 'list'))
    tmpl_files = BaseInitList(path.temp1, path.temp2, path.temp3)
    tmpl_data = BaseInitList(*map(loads, tmpl_files))
    
    for package, v0 in data_r.items():
        if package == '': continue
        print(package, ':di')
        
        target_dir = f'{widgets_dir}/{package.replace(".", "/").lower()}'
        target_files = BaseInitList(
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
    shutil.copyfile(path.temp4, f'{widgets_dir}/readme.md')
    shutil.copyfile(path.temp5, f'{widgets_dir}/__init__.py')


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


def _generate_base(file_i: str, file_o: str) -> None:
    # there is no placeholders in file_i. we just copy file_i to file_o.
    shutil.copyfile(file_i, file_o)


def _generate_init(tmpl_i: str, file_o: str, package: str) -> None:
    # tmpl: 'template'
    # kwargs: {'package': <str>}
    dumps(
        tmpl_i.format(QMLTYPE=package).strip(),
        file_o
    )


def _generate_list(tmpl_i: str, file_o: str, data: T.WidgetData) -> None:
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
    
    widgets_dict = {}  # type: T.WidgetSheetData2
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
        _sort_formatted_list(widgets_dict, (base_component,))
    )).strip(), file_o)
