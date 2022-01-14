import os

from ..base import _do_recursion
from ...models import *


# noinspection PyShadowingNames
def chown(path, user=None, group=None, recursive: bool = False):
    """
    Overview:
        Set the owner of file.

    Arguments:
        - path (:obj:`str`): Path of the file going to set owner.
        - user (:obj:`object`): User object of the user going to be set, \
            default is ``None`` which means do not change user.
        - group (:obj:`object`): Group object of the group going to be set, \
            default is ``None`` which means do not change group.
        - recursive (:obj:`bool`): Recursively set the subdirectories or not, \
            default is ``False`` which means only apply to the current file.

    Examples::
        >>> from pysyslimit import chown
        >>> chown('my_file', 'myself', 'mygroup')  # chown myself:mygroup my_file
        >>> chown('my_dir', 'myself', 'mygroup', recursive=True)  # chown -R myself:mygroup my_dir
    """

    def _single_chown(path_):
        _user_id = SystemUser.loads(user).uid if user else -1
        _group_id = SystemGroup.loads(group).gid if group else -1

        return os.chown(path_, _user_id, _group_id)

    return _do_recursion(path, _single_chown, recursive)
