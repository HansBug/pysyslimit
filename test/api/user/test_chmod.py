import shutil

import pytest

from pysyslimit.api.permission.chmod import *
from pysyslimit.models import FilePermission


@pytest.mark.unittest
class TestApiUserChmod:
    def test_chmods_simple(self):
        path = "./tempFile"
        try:
            os.mknod(path)

            chmod(path, 0)
            assert FilePermission.load_from_file(path) == FilePermission.loads('---------')

            chmod_add(path, "777")
            assert FilePermission.load_from_file(path) == FilePermission.loads('rwxrwxrwx')

            chmod_del(path, "------rwx")
            assert FilePermission.load_from_file(path) == FilePermission.loads('rwxrwx---')
        finally:
            os.remove(path)

    def test_chmods_recursive(self):
        os.makedirs('./1/2/3')
        os.mknod('./1/2/3/file')
        try:
            chmod('./1', 'rwxrwxrwx', recursive=True)
            assert FilePermission.load_from_file('./1') == FilePermission.loads('rwxrwxrwx')
            assert FilePermission.load_from_file('./1/2') == FilePermission.loads('rwxrwxrwx')
            assert FilePermission.load_from_file('./1/2/3') == FilePermission.loads('rwxrwxrwx')
            assert FilePermission.load_from_file('./1/2/3/file') == FilePermission.loads('rwxrwxrwx')

            chmod_del('./1/2', '-w--w--w-', recursive=True)
            assert FilePermission.load_from_file('./1') == FilePermission.loads('rwxrwxrwx')
            assert FilePermission.load_from_file('./1/2') == FilePermission.loads('r-xr-xr-x')
            assert FilePermission.load_from_file('./1/2/3') == FilePermission.loads('r-xr-xr-x')
            assert FilePermission.load_from_file('./1/2/3/file') == FilePermission.loads('r-xr-xr-x')

            chmod('./1', '---------')
            assert FilePermission.load_from_file('./1') == FilePermission.loads('---------')
            assert FilePermission.load_from_file('./1/2') == FilePermission.loads('r-xr-xr-x')
            assert FilePermission.load_from_file('./1/2/3') == FilePermission.loads('r-xr-xr-x')
            assert FilePermission.load_from_file('./1/2/3/file') == FilePermission.loads('r-xr-xr-x')

            chmod_add('./1', 'rw-rw-rw-', recursive=True)
            assert FilePermission.load_from_file('./1') == FilePermission.loads('rw-rw-rw-')
            assert FilePermission.load_from_file('./1/2') == FilePermission.loads('rwxrwxrwx')
            assert FilePermission.load_from_file('./1/2/3') == FilePermission.loads('rwxrwxrwx')
            assert FilePermission.load_from_file('./1/2/3/file') == FilePermission.loads('rwxrwxrwx')
        finally:
            shutil.rmtree('./1')
