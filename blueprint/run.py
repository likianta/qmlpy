import sys
sys.path.insert(0, '..')

from functools import partial

from argsense import cli
import lk_logger  # noqa

from blueprint.src import qml_modules_indexing, template_generator
from blueprint.src import io


@cli.cmd()
def indexing_qml_modules(steps='1234'):
    """
    kwargs:
        steps:
            pick several steps to execute. the value could be any combination -
            from '1', '2', '3', etc. to '134', '1234', etc.
            be noticed it is order sensitive. ('1234' is different from '4321')
    """
    steps_to_exec = {
        '1': partial(qml_modules_indexing.step1, *io.no1),
        '2': partial(qml_modules_indexing.step2, *io.no2),
        '3': partial(qml_modules_indexing.step3, *io.no3, io.qtdoc_dir),
        '4': partial(qml_modules_indexing.step4, *io.no4),
    }
    for k in steps:
        steps_to_exec[k]()


@cli.cmd()
def list_all_group_properties():
    """
    find all possible "group-type" properties.
    the list will be saved in `~/blueprint/resources/other/group_props.json`.
    it is a reference for you to write your own template. -- see also -
    `qmlpy.property.group.api`.
    """
    template_generator.list_all_group_properties.main(
        strip_unrecognized_properties=False,
        use_snake_case=True,
    )


if __name__ == '__main__':
    cli.run()
