import where

from ...utils import *


class GroupdelExecuteException(ExecuteException):
    """
    Overview:
        Exception class of ``groupdel`` command, \
        inherited from :class:`pysyslimit.utils.ExecuteException`.
    """
    pass


def groupdel(
        group_name,
        chroot_dir=None, force=False,
        safe=False
):
    """
    Overview:
        Delete an existing group.
    
    Arguments:
        - group_name: Name of the group.
        - chroot_dir: Root entry directory.
        - force: Force delete.
        - safe: Safe mode (no error information when error)

    Returns:
        - success: Delete success or not.

    Examples::
        >>> from pysyslimit import groupdel
        >>> groupdel('mygroup')  # groupdel mygroup
    """
    _groupdel_cmd = where.first('groupdel')
    if not _groupdel_cmd:
        raise EnvironmentError('No groupdel executable found.')
    _args = [_groupdel_cmd]

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
