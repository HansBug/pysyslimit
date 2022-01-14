import where

from ...models import *
from ...utils import *


class GroupaddExecuteException(ExecuteException):
    """
    Overview:
        Exception class of ``groupadd`` command, \
        inherited from :class:`pysyslimit.utils.ExecuteException`.
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
    Overview:
        Create a new group.
    
    Arguments:
        - group_name: Name of the new group.
        - force: Foce create this group.
        - gid: Gid of this group.
        - non_unique: Not unique group.
        - password: Password of the group.
        - system: Create as system-leveled group.
        - chroot_dir: Root entry directory.
        - extra_users: Use extra user database.
        - safe: Safe mode (no error information when error)

    Returns:
        - group: Created group object.

    Examples::
        >>> from pysyslimit import groupadd
        >>> groupadd('mygroup')  # groupadd mygroup
    """
    _groupadd_cmd = where.first('groupadd')
    if not _groupadd_cmd:
        raise EnvironmentError('No groupadd executable found.')
    _args = [_groupadd_cmd]

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
