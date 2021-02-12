import where

from pysystem.models import *
from pysystem.utils import *


class UseraddExecuteException(ExecuteException):
    """
    useradd指令执行异常类
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
    添加用户
    :param user_name: 用户名
    :param uid: 指定用户id
    :param primary_group: 用户组
    :param groups: 用户附加组
    :param password: 用户密码
    :param system: 创建系统用户
    :param comment: 用户标签
    :param user_group: 创建同名用户组
    :param no_user_group: 不创建同名用户组
    :param create_home: 创建同名home路径
    :param no_create_home: 不创建同名home路径
    :param home_dir: home路径地址
    :param base_dir: 用户base路径地址
    :param shell: 用户shell
    :param chroot_dir: root入口点路径
    :param selinux_user: 删除映射用户
    :param extra_users: 额外用户数据库
    :param safe: 安全模式（出错不抛出异常）
    :return: 创建的用户对象
    """
    useradd_exec = where.first('useradd')
    if not useradd_exec:
        raise EnvironmentError('No useradd executable found.')
    _args = [useradd_exec]

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
