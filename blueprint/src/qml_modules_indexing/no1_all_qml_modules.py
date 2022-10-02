from bs4 import BeautifulSoup
from lk_utils import dumps
from lk_utils import loads

from ..io import T


def main(file_i: str, file_o: str) -> None:
    """
    file_i and file_o are suggested using from `..io.path.step1`.
    """
    soup = BeautifulSoup(loads(file_i), 'html.parser')
    container = soup.find('table', 'annotated')
    
    writer: T.JsonData1 = {
        'module_group': {},
        'module'      : {},
    }
    
    extra_words = ['Qt', 'Quick', 'Qml', 'Win', 'Labs', '5Compat']
    #   '5Compat': (2021-10-29) 升级到 qt6 后, 有一些兼容模块的命名的词尾带上了
    #       "5compat" 的字样. 我们把它调整为 "5Compat".
    
    # noinspection PyTypeChecker
    for e in container.find_all('td', 'tblName'):
        """ <td class="tblName">
                <p>
                    <a href="../qtcharts/qtcharts-qmlmodule.html">
                                ^--1---^ ^--2---^
                        Qt Charts QML Types
                        ^---3---^
                    </a>
                </p>
            </td>
            
            -> 1. module_group: 'qtcharts'
               2. module: 'qtcharts'
               3. name: 'Qt Charts'
        """
        link = e.a['href'].split('/')
        # -> ['..', 'qtquickcontrols1', 'qtquick-controls-qmlmodule.html']
        
        module_group_raw = link[1]  # type: str
        # -> 'qtquickcontrols1'
        module_raw = link[2].replace('-qmlmodule.html', '')  # type: str
        # -> 'qtquick-controls'
        
        """ 针对 QtQuick Controls 的处理
        
        背景: Qt 对 QtQuick.Controls 的命名关系有点乱, 如下所示:
            QtQuick.Controls v1:
                module_group = 'qtquickcontrols1'
                module = 'qtquick-controls'
            QtQuick.Controls v2:
                module_group = 'qtquickcontrols'
                module = 'qtquick-controls2'
        我将 v1 舍弃, 只处理 v2, 并将 v2 的命名改为:
                module_group = 'qtquickcontrols'
                module = 'qtquick-controls' (注意去掉了尾部的数字 2)
        
        为什么这样做:
            以 Button 为例, v1 的 Button 继承于 FocusScope, v2 的 Button 继承于
            AbstractButton. 我的设计的前提是只使用 'qtquickcontrols' 和
            'qtquick-controls', 那么在这种情况下, 二者就只能保留其中一个模组. 因
            此我保留了 v2, 后续解析和分析继承关系也都基于 v2 继续.
        """
        if module_group_raw == 'qtquickcontrols1':
            continue
        if module_raw == 'qtquick-controls2':
            module_raw = 'qtquick-controls'
        
        mini_lexicon = (e.a.text
                        .replace(' QML Types', '')
                        .replace('Qt Quick', 'QtQuick')
                        .replace('Qt3DAnimation', 'Animation')
                        .replace('Web', 'Web ')
                        .title())  # type: str
        """ 解释一下上面的 mini_lexicon 的处理逻辑.
            
            mini_lexicon 为 module_group 和 module 提供一个小型词典, 该词典可用
            于帮助调整 module_group 和 module 的大小写格式.
            例如:
                调整前:
                    module_group: 'qtcharts'
                    module: 'qtcharts'
                调整后:
                    module_group: 'QtCharts'
                    module: 'QtCharts'
            mini_lexicon 来源于 `e.a.text`, 在考虑到实际情况中, 有许多细节需要重
            新调整, 所以我们才要对 mini_lexicon 进行诸多处理, 才能为
            module_group 和 module 所用:
                1. `replace(' QML Types', '')`: 把不必要的词尾去掉.
                2. `replace('Qt Quick', 'QtQuick')`: 遵循模块的写法规范.
                3. `replace('Qt3DAnimation', 'Animation')`: 针对 'Qt 3D
                    Qt3DAnimation' 的处理. 这个貌似是官方的写法有点问题, 所以我
                    把 'Qt3DAnimation' 改成了 'Animation'.
                4. `replace('Web', 'Web ')`: 为了将 'WebEngine' 拆分成
                    'Web Engine', 需要 `mini_lexicon` 提供这两个独立的单词.
                5. `title()`: 将首字母大写, 非首字母小写. 例如:
                    1. 'Qt NFS' -> 'Qt Nfc'
                    2. 'Qt QML' -> 'Qt Qml'
                    
            此外还有一些其他问题:
                1. module_group = 'qtwinextras' 的 `e.a.text` 是
                    'Qt Windows Extras', 该问题不属于 mini_lexicon 的处理范畴.
                    我使用 `extra_words` 变量解决了这个问题. 见 extra_words 的定
                    义.
        """
        
        words = [x.title() for x in mini_lexicon.split(' ') if len(x) > 1]
        # -> ['QtQuick', 'Controls']
        module_group_fmt = _correct_module_lettercase(
            module_group_raw, extra_words + words
        )
        module_fmt = _correct_module_lettercase(
            module_raw, extra_words + words
        )
        
        writer['module_group'][module_group_raw] = module_group_fmt
        writer['module'][module_raw] = module_fmt
    
    dumps(writer, file_o)


def _correct_module_lettercase(module: str, words: list) -> str:
    module = module.replace('-', '.').rstrip(' 12')
    #   'qtquick-controls2' -> 'qtquick.controls'
    for w in words:
        module = module.replace(w.lower(), w)
    #   'qtquick.controls' -> 'QtQuick.Controls'
    
    if '.Labs.' in module:
        a, b = module.split('.', 1)
        module = a + '.' + b.lower()
        # -> 'QtQuick.labs.calendar'
    
    return module
