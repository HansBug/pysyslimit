import where

from ...models import *
from ...utils import *


class UseraddExecuteException(ExecuteException):
    """
    Overview:
        Exception class of ``useradd`` command, \
        inherited from :class:`pysyslimit.utils.ExecuteException`.
    """
    pass


def useradd(
        user_name, uid=None, primary_group=None, groups=None,
        password=None, system=None, comment=None,
        user_group=None, no_user_group=None,
        create_home=None, no_create_home=None,
        home_dir=None, base_dir=None, shell=None,
        chroot_dir=None, selinux_user=None, extra_users=None,
        safe=False
):
    """
    Overview:
        Create a new user.
    
    Arguments:
        - user_name: Name of the user.
        - uid: Uid of the user.
        - primary_group: Primary group of the user.
        - groups: Append groups of the user.
        - password: Password of the user.
        - system: Create as system user or not.
        - comment: Comment information of the user.
        - user_group: Create a user group with the same name or not.
        - no_user_group: Do not create a user group.
        - create_home: Create a home path.
        - no_create_home: Do not create home path.
        - home_dir: Directory of the home path.
        - base_dir: Base directory of the user.
        - shell: User's shell.
        - chroot_dir: User's chroot path.
        - selinux_user: Remove linux mapping user.
        - extra_users: Use extra user database.
        - safe: Safe mode (no error message when error)

    Returns:
        - user: Created user object.

    Examples::
        >>> from pysyslimit import useradd
        >>> useradd("myself")  # useradd myself
    """
    _useradd_cmd = where.first('useradd')
    if not _useradd_cmd:
        raise EnvironmentError('No useradd executable found.')
    _args = [_useradd_cmd]

    if system:  # 创建系统账户
        _args += ["--system"]
    if user_group:  # 创建同名用户组
        _args += ["--user-group"]
    if no_user_group:  # 不创建同名用户组
        _args += ["--no-user-group"]
    if create_home:  # 创建同名home路径
        _args += ["--create-home"]
    if no_create_home:  # 不创建同名home路径
        _args += ["--no-create-home"]
    if extra_users:  # 额外用户
        _args += ["--extrausers"]

    if uid is not None:  # 指定uid
        _args += ["--uid", uid]
    if password:  # 指定密码
        _args += ["--password", password]
    if comment:  # 账户备注
        _args += ["--comment", comment]
    if primary_group:  # 指定主用户组
        _args += ["--gid", primary_group]
    if groups:  # 指定附加用户组
        _args += ["--groups", ",".join([str(_group) for _group in groups])]

    if home_dir:  # 登录主路径
        _args += ["--home-dir", home_dir]
    if base_dir:  # 用户主路径
        _args += ["--base-dir", base_dir]
    if shell:  # 用户shell
        _args += ["--shell", shell]

    if chroot_dir:  # root工作路径
        _args += ["--root", chroot_dir]
    if selinux_user:  # selinux user
        _args += ["--selinux_user"]

    _args += [user_name]  # 用户名

    try:
        execute_process(_args, cls=UseraddExecuteException)
    except UseraddExecuteException as _e:
        if not safe:
            raise _e
        return None

    return SystemUser(name=user_name)
