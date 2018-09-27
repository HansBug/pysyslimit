import os

from pysystem.models import *


# noinspection PyShadowingNames
def chown(path, user=None, group=None):
    """
    修改文件拥有者权限
    :param path: 文件路径
    :param user: 用户
    :param group: 用户组
    :return: None
    """
    if user is None:
        _user_id = -1
    else:
        if not isinstance(user, SystemUser):
            user = SystemUser.loads(user)
        _user_id = user.uid

    if group is None:
        _group_id = -1
    else:
        if not isinstance(group, SystemGroup):
            group = SystemGroup.loads(group)
        _group_id = group.gid

    return os.chown(path, _user_id, _group_id)
