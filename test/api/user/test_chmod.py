import shutil

import pytest

from pysyslimit.api.authority.chmod import *
from pysyslimit.models import FileAuthority


@pytest.mark.unittest
class TestApiUserChmod:
    def test_chmods_simple(self):
        path = "./tempFile"
        try:
            os.mknod(path)

            chmod(path, 0)
            assert FileAuthority.load_from_file(path) == FileAuthority.loads('---------')

            chmod_add(path, "777")
            assert FileAuthority.load_from_file(path) == FileAuthority.loads('rwxrwxrwx')

            chmod_del(path, "------rwx")
            assert FileAuthority.load_from_file(path) == FileAuthority.loads('rwxrwx---')
        finally:
            os.remove(path)

    def test_chmods_recursive(self):
        os.makedirs('./1/2/3')
        os.mknod('./1/2/3/file')
        try:
            chmod('./1', 'rwxrwxrwx', recursive=True)
            assert FileAuthority.load_from_file('./1') == FileAuthority.loads('rwxrwxrwx')
            assert FileAuthority.load_from_file('./1/2') == FileAuthority.loads('rwxrwxrwx')
            assert FileAuthority.load_from_file('./1/2/3') == FileAuthority.loads('rwxrwxrwx')
            assert FileAuthority.load_from_file('./1/2/3/file') == FileAuthority.loads('rwxrwxrwx')

            chmod_del('./1/2', '-w--w--w-', recursive=True)
            assert FileAuthority.load_from_file('./1') == FileAuthority.loads('rwxrwxrwx')
            assert FileAuthority.load_from_file('./1/2') == FileAuthority.loads('r-xr-xr-x')
            assert FileAuthority.load_from_file('./1/2/3') == FileAuthority.loads('r-xr-xr-x')
            assert FileAuthority.load_from_file('./1/2/3/file') == FileAuthority.loads('r-xr-xr-x')

            chmod('./1', '---------')
            assert FileAuthority.load_from_file('./1') == FileAuthority.loads('---------')
            assert FileAuthority.load_from_file('./1/2') == FileAuthority.loads('r-xr-xr-x')
            assert FileAuthority.load_from_file('./1/2/3') == FileAuthority.loads('r-xr-xr-x')
            assert FileAuthority.load_from_file('./1/2/3/file') == FileAuthority.loads('r-xr-xr-x')

            chmod_add('./1', 'rw-rw-rw-', recursive=True)
            assert FileAuthority.load_from_file('./1') == FileAuthority.loads('rw-rw-rw-')
            assert FileAuthority.load_from_file('./1/2') == FileAuthority.loads('rwxrwxrwx')
            assert FileAuthority.load_from_file('./1/2/3') == FileAuthority.loads('rwxrwxrwx')
            assert FileAuthority.load_from_file('./1/2/3/file') == FileAuthority.loads('rwxrwxrwx')
        finally:
            shutil.rmtree('./1')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
