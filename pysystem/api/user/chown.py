import os

from pysystem.api.base import do_recursive
from pysystem.models import *


# noinspection PyShadowingNames
def chown(path, user=None, group=None, recursive: bool = False):
    """
    修改文件拥有者权限
    :param path: 文件路径
    :param user: 用户
    :param group: 用户组
    :param recursive: apply to all recursive paths
    :return: None
    """

    def _single_chown(path_):
        _user_id = SystemUser.loads(user).uid if user else -1
        _group_id = SystemGroup.loads(group).gid if group else -1

        return os.chown(path_, _user_id, _group_id)

    return do_recursive(path, _single_chown, recursive)
