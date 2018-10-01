from pysystem.utils import *


class GroupdelExecuteException(ExecuteException):
    """
    groupdel指令执行异常类
    """
    pass


def groupdel(
        name,
        chroot_dir=None, force=False,
        safe=False
):
    """
    groupdel命令
    :param name: 组名
    :param chroot_dir: root入口点路径
    :param force: 强制创建
    :param safe: 安全模式（出错不抛出异常）
    :return: 是否删除成功
    """
    _args = []

    if chroot_dir:
        _args += ["--chroot_dir", chroot_dir]
    if force:
        _args += ["--force"]

    _args = ["groupdel"] + _args
    _args += [name]

    try:
        execute_process(_args, cls=GroupdelExecuteException)
    except GroupdelExecuteException as _e:
        if not safe:
            raise _e
        return False

    return True
