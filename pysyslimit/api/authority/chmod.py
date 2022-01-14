import os

from pysyslimit.api.base import do_recursive
from pysyslimit.models import *


def chmod(path, mod, recursive: bool = False):
    """
    设置文件权限
    :param path: 文件路径
    :param mod: 权限
    :param recursive: apply to all recursive paths
    :return: None
    """

    def _single_chmod(path_):
        return os.chmod(path_, int(FileAuthority.loads(mod)))

    return do_recursive(path, _single_chmod, recursive)


def chmod_add(path, mod, recursive: bool = False):
    """
    权限增加
    :param path: 文件路径
    :param mod: 权限
    :param recursive: apply to all recursive paths
    :return: None
    """

    def _single_chmod_add(path_):
        _origin_mode = FileAuthority.load_from_file(path_)
        _add_mode = FileAuthority.loads(mod)
        return chmod(path_, _origin_mode + _add_mode)

    return do_recursive(path, _single_chmod_add, recursive)


def chmod_del(path, mod, recursive: bool = False):
    """
    权限删除
    :param path: 文件路径
    :param mod: 权限
    :param recursive: apply to all recursive paths
    :return: None
    """

    def _single_chmod_del(path_):
        _origin_mode = FileAuthority.load_from_file(path_)
        _del_mode = FileAuthority.loads(mod)
        return chmod(path_, _origin_mode - _del_mode)

    return do_recursive(path, _single_chmod_del, recursive)
