from __future__ import annotations

if True:
    import sys
    sys.path.insert(0, '..')

import os
from functools import partial

import lk_logger  # noqa
from argsense import cli
from lk_utils.filesniff import normpath

from blueprint.src.io import path
from blueprint.src import qml_modules_indexing
from blueprint.src import template_generator


@cli.cmd()
def indexing_qml_modules(steps='1234'):
    """
    kwargs:
        steps:
            pick several steps to execute. the value could be any combination -
            from '1', '2', '3', etc. to '134', '1234', etc.
            be noticed it is order sensitive. ('1234' is different from '4321')
    """
    if '3' in steps:
        if path.qtdoc_src is None:
            print('the qtdoc root is not set. please manually fill it below. '
                  '(the path is usually like "<Qt>/Docs/Qt-5.15.2/qtdoc".)')
            path.qtdoc_src = normpath(input('input path: '))
            assert os.path.exists(path.qtdoc_src) and \
                   path.qtdoc_src.endswith('qtdoc')
    
    # noinspection PyArgumentList
    steps_to_exec = {
        '1': partial(qml_modules_indexing.step1, *path.step1),
        '2': partial(qml_modules_indexing.step2, *path.step2),
        '3': partial(qml_modules_indexing.step3, *path.step3),
        '4': partial(qml_modules_indexing.step4, *path.step4),
    }
    for k in steps:
        steps_to_exec[k]()


@cli.cmd()
def generate_properties_api(type_: str):
    """
    args:
        type_: 'basic' or 'group'
    """
    if type_ == 'basic':
        template_generator.properties.list_basic_types(
            file_i=path.json3, file_o=path.prop1
        )
    else:
        template_generator.properties.list_group_types(
            file_i=path.json3, file_o=path.prop2,
            strip_unrecognized_properties=False,
            analyse=True,
        )


@cli.cmd()
def generate_widget_props_api(cast_safe=True):
    """
    this generates (or overwrites):
        `~/qmlpy/widgets/widget_props.py`
    """
    template_generator.widgets.generate_all_widget_props(
        cast_safe=cast_safe,
    )


@cli.cmd()
def generate_widgets_api():
    """
    this generates:
        `~/qmlpy/widgets/api/**`
        
    notice: for safe consideration, you should [red]manually[/] remove the -
    target api dir before executing this command. otherwise, this command will -
    be force exited at start.
    """
    # template_generator.widgets.generate_all_widget_props()
    template_generator.widgets.generate_widgets_api()


if __name__ == '__main__':
    cli.run()
