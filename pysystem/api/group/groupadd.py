import where

from pysystem.models import *
from pysystem.utils import *


class GroupaddExecuteException(ExecuteException):
    """
    groupadd指令执行异常类
    """
    pass


def groupadd(
        group_name,
        force=False, gid=None, non_unique=False,
        password=None, system=False, chroot_dir=None,
        extra_users=False,
        safe=False
):
    """
    groupadd命令
    :param group_name: 组名
    :param force: 强制创建
    :param gid: 组id
    :param non_unique: 运行不唯一id
    :param password: 组密码
    :param system: 创建系统组
    :param chroot_dir: root入口点路径
    :param extra_users: 额外用户数据库
    :param safe: 安全模式（出错不抛出异常）
    :return: 创建的组对象
    """
    groupadd_exec = where.first('groupadd')
    if not groupadd:
        raise EnvironmentError('No groupadd executable found.')
    _args = [groupadd_exec]

    if force:
        _args += ["--force"]
    if gid:
        _args += ["--gid", gid]
    if non_unique:
        _args += ["--non-unique"]
    if password:
        _args += ["--password", password]
    if system:
        _args += ["--system"]
    if chroot_dir:
        _args += ["--root", chroot_dir]
    if extra_users:
        _args += ["--extrausers"]

    _args += [group_name]

    try:
        execute_process(_args, cls=GroupaddExecuteException)
    except GroupaddExecuteException as _e:
        if not safe:
            raise _e
        return None

    return SystemGroup(name=group_name)
