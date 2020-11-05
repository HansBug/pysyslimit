import os

from pysystem.models import *


def chmod(path, mod):
    """
    设置文件权限
    :param path: 文件路径
    :param mod: 权限
    :return: None
    """
    return os.chmod(path, int(FileAuthority.loads(mod)))


def chmod_add(path, mod):
    """
    权限增加
    :param path: 文件路径
    :param mod: 权限
    :return: None
    """
    _origin_mode = FileAuthority.load_from_file(path)
    _add_mode = FileAuthority.loads(mod)
    return chmod(path, _origin_mode + _add_mode)


def chmod_del(path, mod):
    """
    权限删除
    :param path: 文件路径
    :param mod: 权限
    :return: None
    """
    _origin_mode = FileAuthority.load_from_file(path)
    _del_mode = FileAuthority.loads(mod)
    return chmod(path, _origin_mode - _del_mode)
