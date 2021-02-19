import pytest

from pysystem.api.authority.chmod import *
from pysystem.models import FileAuthority


@pytest.mark.unittest
class TestApiUserChmod:
    def test_chmod(self):
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


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
