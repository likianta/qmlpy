from collections import defaultdict

from lk_utils import dumps
from lk_utils import loads

from ...io import path


def list_all(file_i: str = path.json3, file_o: str = path.prop1) -> dict:
    """
    args:
        file_i:
            data structure: {
                <module>: {
                    <qmltype>: {
                        'parent': ...,
                        'props': {<prop>: <type>, ...}
                    }, ...                ^----- 我们统计的是这个.
                }, ...
            }
        file_o:
            data structure: [type, ...]. 一个去重后的列表, 按照字母表顺序排列.
            if not given (i.e. using '' or None), will not dump to file.

    return:
        data_w: {type: [(module, qmltype, prop), ...], ...}
    """
    data_r = loads(file_i)
    data_w = defaultdict(set)  # type: dict[str, set[tuple[str, str, str]]]
    
    for k1, v1 in data_r.items():
        for k2, v2 in v1.items():
            for k3, v3 in v2['props'].items():
                # k1: module; k2: qmltype; k3: prop; v3: type
                data_w[v3].add((k1, k2, k3))
    
    [print(i, k) for i, k in enumerate(sorted(data_w.keys()), 1)]
    
    data_w = {k: sorted(data_w[k]) for k in sorted(data_w.keys())}
    if file_o: dumps(data_w, file_o)
    return data_w
