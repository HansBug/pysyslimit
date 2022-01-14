import os


def _do_recursion(path, func, recursive):
    if recursive and os.path.isdir(path):
        for _curdir, _subdirs, _files in os.walk(path):
            func(_curdir)
            for _file in _files:
                func(os.path.join(_curdir, _file))
    else:
        func(path)
