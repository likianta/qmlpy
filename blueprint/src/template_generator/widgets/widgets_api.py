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
    
    # the structure of `data_r` is complex. the following code logic is mainly
    # written and deduced with an observation on `io.json3 > content > key:
    # qtquick`.
    
    print('creating dirs', ':d')
    _create_dirs(api_dir, data_r.keys())
    
    Template = namedtuple('BaseListInit', ('base', 'list', 'init'))
    files_i = Template(path.temp1, path.temp2, path.temp3)
    temp_i = Template(*map(loads, files_i))
    del files_i
    
    for package, v0 in data_r.items():
        if package == '': continue
        print(package, ':di')
        
        dir_o = f'{api_dir}/{package.replace(".", "/").lower()}'
        files_o = Template(
            f'{dir_o}/__base__.py',
            f'{dir_o}/__list__.py',
            f'{dir_o}/__init__.py',
        )
        assert not ospath.exists(files_o.init)
        
        # generate target files
        _generate_base(
            temp_i.base, files_o.base,
            file_o_relpath=files_o.base[len(api_dir) + 1:],
            data=v0, name_2_path=name_2_path
        )
        _generate_list(
            temp_i.list, files_o.list,
            data=v0
        )
        _generate_init(
            temp_i.init, files_o.init,
            package=package
        )
    
    # put 'readme' and '__init__' files in api root dir.
    shutil.copyfile(path.temp4, f'{api_dir}/readme.md')
    shutil.copyfile(path.temp5, f'{api_dir}/__init__.py')


# ------------------------------------------------------------------------------

def _indexing_widget_name_2_package_path(data: T.JsonData3) -> T.Name2Path:
    out: T.Name2Path = {}
    for package, v0 in data.items():
        package_path = package.replace('.', '/').lower()
        for widget_name in v0.keys():
            out[widget_name] = package_path
    return out


def _create_dirs(root_dir: str, packages: t.Iterable[str]):
    """
    notice: element in packages may be empty! remember to filter it.
    """
    if not ospath.exists(root_dir):
        mkdir(root_dir)
    
    dirs_: t.Set[str] = set()
    for pkg in filter(None, packages):
        pkg = pkg.lower()
        tmp = root_dir
        for node in pkg.split('.'):
            tmp += '/' + node
            dirs_.add(tmp)
    
    for d in sorted(dirs_):
        if not ospath.exists(d):
            print(':i', ospath.relpath(d, root_dir))
            mkdir(d)


# -----------------------------------------------------------------------------

def _generate_base(
        temp_i: str,
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
        temp_i.format(ADDITIONAL_IMPORTS='\n'.join(inserted_lines)).strip(),
        file_o
    )


def _generate_list(temp_i: str, file_o: str, data: T.WidgetSheet1) -> None:
    base_component = 'C'
    
    widgets_dict: T.WidgetSheet2 = {}
    widget_temp = dedent('''
        class {WIDGET}({PARENT}, {PROP_SHEET}, {SIGNAL_SHEET}, {FUNC_SHEET}):
            pass
    ''').strip()
    
    for widget_name, v0 in data.items():
        parent_name = v0['parent'] or base_component
        print(widget_name, parent_name, ':i')
        
        widgets_dict[widget_name] = (
            parent_name,
            widget_temp.format(
                WIDGET=widget_name,
                PARENT=parent_name,
                PROP_SHEET=f'P.{widget_name}',
                SIGNAL_SHEET=f'S.{widget_name}',
                FUNC_SHEET=f'F.{widget_name}',
            )
        )
    
        '''
        note: 'C' 'P' 'S' 'F' are names imported from `__base__` file.
        see also:
            - def _generate_base
            - ~/blueprint/resources/widgets_template/__base__.txt
            - ~/qmlpy/widgets/namespace/__qml_namespace__.py
        '''
    
    dumps(temp_i.format(WIDGETS='\n\n\n'.join(
        _sort_formatted_list(widgets_dict, (base_component,))
    )).strip(), file_o)


def _generate_init(temp_i: str, file_o: str, package: str) -> None:
    dumps(
        temp_i.format(QMLTYPE=package).strip(),
        file_o
    )


# -----------------------------------------------------------------------------

def _fix_missing_parents(
        path_src: str,
        data: T.PackageInfo,
        name_2_path: T.Name2Path,
) -> t.Iterator[str]:
    """
    in data, we have a dict:
        {name: {'parent': parent_name, ...}, ...}
    the parent name may not be in the same package, i.e. parent may not in
    `data.keys()`. we need to import them by relative import.
    
    example:
        # data = {'SomeWidget': {'parent': 'Item', ...}, ...}
        from ..qtquick import Item
        class SomeWidget(Item):
            ...
    
    args:
        path_src: should be: 1. relative, 2. directory.
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
            paths[path].add(name)  # it means: from this path import this name.
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
