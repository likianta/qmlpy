"""
terminology:
    package (pakg): the qml importable name. for example 'qtquick',
        'quick.controls', etc.
        we use all snake_case naming style across the whole project.
    component (comp): the qml type name. for example 'Item', 'Rectangle',
        'MouseArea', etc.
    property (prop): qml property name. for example 'border', 'border.width',
        'color', etc.

structure:
    package (pakg)
        component (comp)
            property (prop)
"""
import sys
from lk_utils import relpath
sys.path.insert(0, relpath('../../..'))

import lk_logger  # noqa
from argsense import cli

from blueprint.src import io
from blueprint.src.qml_modules_indexing import no1_all_qml_modules
from blueprint.src.qml_modules_indexing import no2_all_qml_types
from blueprint.src.qml_modules_indexing import no3_all_qml_widgets
from blueprint.src.qml_modules_indexing import no4_all_pyml_widgets


@cli.cmd('all')
def main():
    """
    run all steps (step 1 ~ 4).
    """
    step1()
    step2()
    step3()
    step4()


@cli.cmd()
def step1():
    """
    convert `io.html_1` to `io.json_1`.
    """
    no1_all_qml_modules.main(*io.no1)


@cli.cmd()
def step2():
    """
    convert `io.html_2` to `io.json_2`.
    """
    no2_all_qml_types.main(*io.no2)


@cli.cmd()
def step3():
    """
    convert `io.json_2` to `io.json_3`.
    """
    no3_all_qml_widgets.main(*io.no3, io.qtdoc_dir)


@cli.cmd()
def step4():
    """
    convert `io.json_3` to `io.json_4`.
    """
    no4_all_pyml_widgets.main(*io.no4)


if __name__ == '__main__':
    cli.run()
