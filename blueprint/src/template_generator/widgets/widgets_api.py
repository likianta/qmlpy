import shutil
import typing as t
from collections import defaultdict
from collections import namedtuple
from os import mkdir
from os import path as ospath
from textwrap import dedent

from lk_utils import dumps
from lk_utils import loads
from lk_utils.filesniff import dirpath

from .widget_oriented_props import T as T0
from .widget_oriented_props import _sort_formatted_list
from ...io import path


class T(T0):
    Name2Path = t.Dict[str, str]
    PackageInfo = t.Dict[str, t.TypedDict('WidgetInfo', {
        'parent': str,
        'props' : t.Dict[str, str]
    })]


def main(api_dir: str = path.proj_root + '/qmlpy/widgets/api'):
    data_r: T.JsonData3 = loads(path.json3)
    name_2_path = _indexing_widget_name_2_package_path(data_r)
    
    # data_r 的数据结构比较复杂. 下面的代码逻辑主要基于 `io.json3.<data>.<key
    # :qtquick>` 进行观察和编写.
    
    print('creating dirs', ':d')
    _create_dirs(api_dir, data_r.keys())
    
    BaseInitList = namedtuple('BaseInitList', ('base', 'init', 'list'))
    tmpl_files = BaseInitList(path.temp1, path.temp2, path.temp3)
    tmpl_data = BaseInitList(*map(loads, tmpl_files))
    del tmpl_files
    
    for package, v0 in data_r.items():
        if package == '': continue
        print(package, ':di')
        
        target_dir = f'{api_dir}/{package.replace(".", "/").lower()}'
        target_files = BaseInitList(
            f'{target_dir}/__base__.py',
            f'{target_dir}/__init__.py',
            f'{target_dir}/__list__.py',
        )
        assert not ospath.exists(target_files.init)
        
        # generate target files (__base__, __init__, __list__).
        _generate_base(tmpl_data.base, target_files.base,
                       file_o_relpath=target_files.base[len(api_dir) + 1:],
                       data=v0, name_2_path=name_2_path)
        _generate_init(tmpl_data.init, target_files.init, package=package)
        _generate_list(tmpl_data.list, target_files.list, data=v0)
    
    # put readme and __init__ files in api root dir.
    shutil.copyfile(path.temp4, f'{api_dir}/readme.md')
    shutil.copyfile(path.temp5, f'{api_dir}/__init__.py')


# ------------------------------------------------------------------------------

def _indexing_widget_name_2_package_path(
        data: T.JsonData3
) -> T.Name2Path:
    out: T.Name2Path = {}
    for package, v0 in data.items():
        package_path = package.replace('.', '/').lower()
        for widget_name in v0.keys():
            out[widget_name] = package_path
    return out


def _create_dirs(widgets_dir, packages):
    if not ospath.exists(widgets_dir):
        mkdir(widgets_dir)
    
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
        if not ospath.exists(d):
            print(':i', ospath.relpath(d, widgets_dir))
            mkdir(d)


# -----------------------------------------------------------------------------

def _generate_base(
        tmpl_i: str,
        file_o: str,
        file_o_relpath: str,
        data: T.PackageInfo,
        name_2_path: T.Name2Path,
) -> None:
    inserted_lines = sorted(_fix_missing_parents(
        path_src=dirpath(file_o_relpath),
        data=data,
        name_2_path=name_2_path,
    ))
    dumps(
        tmpl_i.format(ADDITIONAL_IMPORTS='\n'.join(inserted_lines)).strip(),
        file_o
    )


def _generate_init(tmpl_i: str, file_o: str, package: str) -> None:
    # tmpl: 'template'
    # kwargs: {'package': <str>}
    dumps(
        tmpl_i.format(QMLTYPE=package).strip(),
        file_o
    )


def _generate_list(tmpl_i: str, file_o: str, data: T.WidgetSheetData1) -> None:
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


# -----------------------------------------------------------------------------

def _fix_missing_parents(
        path_src: str,
        data: T.PackageInfo,
        name_2_path: T.Name2Path,
) -> t.Iterator[str]:
    """
    args:
        path_src: 1. relative, 2. directory.
    """
    all_parent_names = set()
    for v0 in data.values():
        # be careful: v0['parent'] may be empty string.
        if v0['parent']:
            all_parent_names.add(v0['parent'])
    
    paths = defaultdict(set)
    for name in all_parent_names:
        if name not in data:
            path = name_2_path[name]
            print(f'found missing parent: [cyan]{name}[/]. '
                  f'we can import it from [magenta]{path}[/]', ':r')
            paths[path].add(name)
    if not paths:
        return
    
    def calc_relative_import(src: str, dst: str) -> str:
        """
        example:
            src = 'qtquick/layouts'
            dst = 'ququick/controls'
            return: '..layouts.__list__'
        notice: both src and dst must be directory.
        """
        src = src.split('/')
        dst = dst.split('/')
        while src and dst and src[0] == dst[0]:
            src.pop(0)
            dst.pop(0)
        return '.' + '.' * len(src) + '.'.join(dst + ['__list__'])
    
    for path_dst, names in paths.items():
        rel_imp = calc_relative_import(path_src, path_dst)
        yield 'from {} import {}  # noqa'.format(
            rel_imp, ', '.join(sorted(names))
        )
