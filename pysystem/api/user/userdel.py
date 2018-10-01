from pysystem.utils import *


class UserdelExecuteException(ExecuteException):
    """
    userdel指令执行异常类
    """
    pass


def userdel(
        name,
        force=False, remove_dir=False,
        chroot_dir=None, selinux_user=False,
        safe=False
):
    """
    删除用户
    :param name: 用户名
    :param force: 强制删除
    :param remove_dir: 删除用户路径
    :param chroot_dir: root入口点路径
    :param selinux_user: 删除映射用户
    :param safe: 安全模式（出错不抛出异常）
    :return: 是否成功删除
    """
    _args = []

    if force:  # 强制删除
        _args += ["--force"]
    if remove_dir:  # 删除用户路径
        _args += ["--remove"]
    if chroot_dir:  # root工作路径
        _args += ["--root", chroot_dir]
    if selinux_user:  # selinux user
        _args += ["--selinux_user"]

    _args = ["userdel"] + _args
    _args += [name]

    try:
        execute_process(_args, cls=UserdelExecuteException)
    except UserdelExecuteException as _e:
        if not safe:
            raise _e
        return False

    return True
