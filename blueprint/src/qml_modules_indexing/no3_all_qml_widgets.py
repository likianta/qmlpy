import typing as t
from collections import defaultdict
from os.path import exists

from bs4 import BeautifulSoup
from lk_utils import dumps
from lk_utils import loads

from .no2_all_qml_types import correct_module_lettercase
from ..io import T
from ..io import path


def main(file_i: str, file_o: str,
         qtdoc_dir: str = path.qtdoc_src) -> None:
    """
    file_i and file_o are suggested using from `..io.path.step3`.
    """
    assert qtdoc_dir and exists(qtdoc_dir), (
        'The Qt Docs directory is not specified '
        'or not existed!', qtdoc_dir
    )
    
    reader: T.JsonData2 = loads(file_i)
    # noinspection PyTypeChecker
    writer: T.JsonData3 = defaultdict(
        lambda: defaultdict(lambda: {
            'parent': (),
            'props' : {},
        })
    )
    
    for module, qmltype, file_i in _get_files(reader, qtdoc_dir):
        print(':i', qmltype)
        
        if not exists(file_i):
            print(':v2', 'file not found', qmltype)
            continue
        
        try:
            parent_package, parent_name, props = _parse_file(file_i)
        except Exception as e:
            print(':v4d', 'error happened when parsing file')
            print(':v4l', module, qmltype, file_i)
            raise e
        
        # noinspection PyTypedDict
        writer[module][qmltype]['parent'] = (parent_package, parent_name)
        writer[module][qmltype]['props'].update(props)
    
    dumps(writer, file_o)


def _parse_file(file: str) -> t.Tuple[str, str, dict]:
    soup = BeautifulSoup(loads(file), 'html.parser')
    # 下面以 '{qtdoc_dir}/qtquick/qml-qtquick-rectangle.html' 为例分析 (请在
    # 浏览器中查看此 html, 打开开发者工具.)
    
    parent_package = ''
    parent_name = ''
    props = {}
    
    try:  # get parent
        '''
        <table class="alignedsummary">
            <tr>...</tr>
            # 目标可能在第二个 tr, 也可能在第三个 tr. 例如 Rectangle 和
            # Button 的详情页. 有没有其他情况不太清楚 (没有做相关测试). 安全
            # 起见, 请逐个 tr 进行检查.
            <tr>
                <td class="memItemLeft rightAlign topAlign"> Inherits:</td>
                <td class="memItemRight bottomAlign">
                    <p>
                        <a href="qml-qtquick-item.html">Item</a>
                    </p>
                </td>
            </tr>
            ...
        </table>
        '''
        e = soup.find('table', 'alignedsummary')
        # noinspection PyTypeChecker
        for tr in e.find_all('tr'):
            if tr.td.text.strip() == 'Inherits:':
                td = tr.find('td', 'memItemRight bottomAlign')
                parent_package = correct_module_lettercase(
                    # this snippet is learnt from `.no2_all_qml_types.main.
                    # <var:module>.<related_usages>`
                    '-'.join(td.a['href'].split('-')[1:-1])
                    # e.g. 'qml-qtquick-item.html' -> ['qml', 'qtquick', 'item']
                    #   -> ['qtquick'] -> correct_module_lettercase(...)
                    #   -> 'QtQuick'
                )
                parent_name = td.text.strip()
                break
    except AttributeError:
        pass
    
    try:  # props
        e = soup.find(id='properties')
        e = e.find_next_sibling('ul')
        # noinspection PyTypeChecker
        for li in e.find_all('li'):
            '''
            <li class="fn">
                ...
                    <a href=...>border</a>  # this is `prop`
                    # border 的值的类型是空, 我们用 'group' 替代
                ...
                <ul>
                    <li class="fn">
                        ...
                            <a href=...>border.color</a>  # this is `prop`
                        ...
                        " : color"  # this is `type`
                    </li>
                    ...
                </ul>
            </li>

            References:
                https://blog.csdn.net/Kwoky/article/details/82890689
            '''
            # `p` and `t` means 'property' and 'type'
            p = li.a.text
            try:
                t = li.contents[-1].strip(' :').strip() or 'group'
                #   .strip(' :').strip()
                #       后一个 strip 是为了去除未知的空白符, 比如换行符或者其他
                #       看不见的字符 (后者通常是 html 数据不规范引起的).
                #   or 'group'
                #       对于 border, font, anchors 这种 "属性组", 它们的
                #       `li.contents[-1]` 是一个 '\n'. 也就是说经过 strip 后就变
                #       成了空字符串. 我们会用 'group' 来代替.
            except TypeError:
                '''
                该错误在 Qt 6 中首次出现.
                通常来说, `li.contents` 只会有两种形态:
                    1. [<a>...</a>, str]
                    2. [<a>...</a>, <ul><li>...</li><li>...</li>...</ul>, '\n']
                我们在 try 块中处理的就是以上两种情况.
                第三种情况出现在: qt 添加了拟案属性, 其标签树如下所示:
                    <li>
                        <a>...</a>
                        '...'  # 这里是原本要获取的属性类型
                        <code> (preliminary)</code>  # 新增加了一个 code 标签
                    </li>
                所以我们改用 `li.contents[-2]` 来获得目标.
                '''
                assert len(li.contents) == 3
                assert li.contents[-1].text == ' (preliminary)'
                t = li.contents[-2].strip(' :').strip()
                print(':v2', 'found a preliminary type', parent_name, t, file)
            props[p] = t
    except AttributeError:
        pass
    except Exception as e:
        breakpoint()
        raise e
    
    return parent_package, parent_name, props


def _get_files(data: dict, dir_i: str) -> t.Iterator[t.Tuple[str, str, str]]:
    for module_group, node1 in data.items():
        for module, node2 in node1.items():
            for qmltype, relpath in node2.items():
                yield module, qmltype, dir_i + '/' + relpath
