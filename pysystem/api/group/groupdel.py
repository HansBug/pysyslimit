import where

from pysystem.utils import *


class GroupdelExecuteException(ExecuteException):
    """
    groupdel指令执行异常类
    """
    pass


def groupdel(
        group_name,
        chroot_dir=None, force=False,
        safe=False
):
    """
    groupdel命令
    :param group_name: 组名
    :param chroot_dir: root入口点路径
    :param force: 强制创建
    :param safe: 安全模式（出错不抛出异常）
    :return: 是否删除成功
    """
    groupdel_exec = where.first('groupdel')
    if not groupdel_exec:
        raise EnvironmentError('No groupdel executable found.')
    _args = [groupdel_exec]

    if chroot_dir:
        _args += ["--chroot_dir", chroot_dir]
    if force:
        _args += ["--force"]

    _args += [group_name]

    try:
        execute_process(_args, cls=GroupdelExecuteException)
    except GroupdelExecuteException as _e:
        if not safe:
            raise _e
        return False

    return True
