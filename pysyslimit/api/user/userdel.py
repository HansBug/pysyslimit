import where

from ...utils import *


class UserdelExecuteException(ExecuteException):
    """
    Overview:
        Exception class of ``userdel`` command, \
        inherited from :class:`pysyslimit.utils.ExecuteException`.
    """
    pass


def userdel(
        user_name,
        force=False, remove_dir=False,
        chroot_dir=None, selinux_user=False,
        safe=False
):
    """
    Overview:
        Delete an existing user.
    
    Arguments:
        - user_name: Name of the user.
        - force: Force delete.
        - remove_dir: Remove the directory of user or not.
        - chroot_dir: Root entry path.
        - selinux_user: Remove the mapping user.
        - safe: Safe mode (no error information when error)

    Returns:
        - success: Delete success or not.

    Examples::
        >>> from pysyslimit import userdel
        >>> userdel('myself')  # userdel myself
    """
    _userdel_cmd = where.first('userdel')
    if not _userdel_cmd:
        raise EnvironmentError('No userdel executable found.')
    _args = [_userdel_cmd]

    if force:  # 强制删除
        _args += ["--force"]
    if remove_dir:  # 删除用户路径
        _args += ["--remove"]
    if chroot_dir:  # root工作路径
        _args += ["--root", chroot_dir]
    if selinux_user:  # selinux user
        _args += ["--selinux_user"]

    _args += [user_name]

    try:
        execute_process(_args, cls=UserdelExecuteException)
    except UserdelExecuteException as _e:
        if not safe:
            raise _e
        return False

    return True
