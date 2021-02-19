import pytest

from pysystem.api.authority.chmod import *


@pytest.mark.unittest
class TestApiUserChmod:
    def test_chmod(self):
        path = "./tempFile"
        try:
            os.mknod(path)

            chmod(path, 0)
            assert (os.stat(path).st_mode & 0o777) == 0

            chmod_add(path, "777")
            assert (os.stat(path).st_mode & 0o777) == 0o777

            chmod_del(path, "------rwx")
            assert (os.stat(path).st_mode & 0o777) == 0o770
        finally:
            os.remove(path)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
