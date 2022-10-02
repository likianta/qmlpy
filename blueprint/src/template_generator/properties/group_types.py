from __future__ import annotations

import typing as t
from collections import defaultdict

from lk_utils import dumps
from lk_utils import loads

from ...common import camel_2_snake_case
from ...io import T as T0
from ...io import path


class T(T0):
    PropName = str
    PropSubName = str
    PropType = str
    
    Props = t.Dict[PropName, PropType]
    GroupNames = t.Set[PropName]
    GroupAttrs = t.Dict[PropName, t.Dict[PropSubName, PropType]]


def list_all(
        file_i: str = path.json3,
        file_o: str = path.prop2,
        strip_unrecognized_properties=True,
        analyse=False,
) -> dict[str, dict[str, str]]:
    data_r: T.JsonData3 = loads(file_i)
    
    group_names: T.GroupNames = set()
    #   e.g. {'width', 'height', ...}
    group_attrs: T.GroupAttrs = defaultdict(dict)
    #   e.g. {'border': {'width': 1, 'color': 'red', ...}, ...}
    
    for v0 in data_r.values():
        for v1 in v0.values():
            props: T.Props = v1['props']
            
            for k, v in props.items():
                if v == 'group':
                    group_names.add(k)
                elif '.' in k:
                    name, attr = k.split('.', 1)
                    group_attrs[name][attr] = v
    
    if strip_unrecognized_properties:
        # if k in `group_attrs` but not in `group_names`, remove it.
        to_be_popped = tuple(x for x in group_attrs.keys()
                             if x not in group_names)
        [group_attrs.pop(x) for x in to_be_popped]
    
    # sort keys and reformat keys.
    group_attrs, temp = defaultdict(dict), group_attrs
    for k0 in sorted(temp):
        for k1 in sorted(temp[k0]):
            # use snake case.
            new_k0 = camel_2_snake_case(k0)
            new_k1 = camel_2_snake_case(k1)
            group_attrs[new_k0][new_k1] = temp[k0][k1]
    
    if file_o:
        dumps(group_attrs, file_o)
    if analyse:
        _analyse(group_attrs)
        
    return group_attrs


def generate_sheet():
    pass


def _analyse(data: T.GroupAttrs) -> None:
    types = set()
    for v0 in data.values():
        for v1 in v0.values():
            types.add(v1)
    for t in sorted(types):
        print(t)
