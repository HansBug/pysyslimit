import grp
import pwd


def _all_uid():
    """
    获取全部用户uid
    :return: 全部用户uid列表
    """
    return [_user.pw_uid for _user in pwd.getpwall()]


def _all_gid():
    """
    获取全部用户组gid
    :return: 全部用户组gid列表
    """
    return [_group.gr_gid for _group in grp.getgrall()]
