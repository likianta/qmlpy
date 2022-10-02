from collections import defaultdict

from lk_utils import dumps
from lk_utils import loads

from ..common import camel_2_snake_case
from ..io import T


def main(file_i: str, file_o: str) -> None:
    """
    file_i and file_o are suggested using from `..io.path.step4`.
    """
    data_i: T.JsonData3 = loads(file_i)
    data_o: T.JsonData4 = defaultdict(lambda: defaultdict(dict))
    for module, v1 in data_i.items():
        for type_, v2 in v1.items():
            package = camel_2_snake_case(module)
            #   e.g. 'qtquick.Controls' -> 'qtquick.controls'
            widget = type_
            #   e.g. 'MouseArea'
            
            data_o[package][widget] = {
                'parent': v2['parent'],
                'props' : dict(zip(
                    map(camel_2_snake_case, v2['props'].keys()),
                    v2['props'].values()
                ))
            }
    dumps(data_o, file_o)
