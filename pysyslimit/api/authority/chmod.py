import os

from ..base import _do_recursion
from ...models import *


def chmod(path: str, mod, recursive: bool = False):
    """
    Overview:
        Set the permission of file.

    Arguments:
        - path (:obj:`str`): Path of the file going to set permission.
        - mod (:obj:`object`): Permission information object.
        - recursive (:obj:`bool`): Recursively set the subdirectories or not, \
            default is ``False`` which means only apply to the current file.

    Examples::
        >>> from pysyslimit import chmod
        >>> chmod('my_file', '777')  # chmod 777 my_file
        >>> chmod('my_dir', '777', recursive=True)  # chmod -R 777 my_dir
    """

    def _single_chmod(path_):
        return os.chmod(path_, int(FileAuthority.loads(mod)))

    return _do_recursion(path, _single_chmod, recursive)


def chmod_add(path, mod, recursive: bool = False):
    """
    Overview:
        Append the permission of file.

    Arguments:
        - path (:obj:`str`): Path of the file going to append permission.
        - mod (:obj:`object`): Permission information object.
        - recursive (:obj:`bool`): Recursively set the subdirectories or not, \
            default is ``False`` which means only apply to the current file.

    Examples::
        >>> from pysyslimit import chmod_add
        >>> chmod_add('my_file', '600')  # chmod +600 my_file
        >>> chmod_add('my_dur', '600', recursive=True)  # chmod -R +600 my_dir
    """

    def _single_chmod_add(path_):
        _origin_mode = FileAuthority.load_from_file(path_)
        _add_mode = FileAuthority.loads(mod)
        return chmod(path_, _origin_mode + _add_mode)

    return _do_recursion(path, _single_chmod_add, recursive)


def chmod_del(path, mod, recursive: bool = False):
    """
    Overview:
        Remove the permission of file.

    Arguments:
        - path (:obj:`str`): Path of the file going to remove permission.
        - mod (:obj:`object`): Permission information object.
        - recursive (:obj:`bool`): Recursively set the subdirectories or not, \
            default is ``False`` which means only apply to the current file.

    Examples::
        >>> from pysyslimit import chmod_del
        >>> chmod_del('my_file', '600')  # chmod -600 my_file
        >>> chmod_del('my_dur', '600', recursive=True)  # chmod -R -600 my_dir
    """

    def _single_chmod_del(path_):
        _origin_mode = FileAuthority.load_from_file(path_)
        _del_mode = FileAuthority.loads(mod)
        return chmod(path_, _origin_mode - _del_mode)

    return _do_recursion(path, _single_chmod_del, recursive)
