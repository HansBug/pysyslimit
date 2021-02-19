import os
import pwd

import pytest

from pysystem.api.authority.chown import chown
from pysystem.models import SystemUser


@pytest.mark.unittest
class TestApiAuthorityChown:
    def test_user_root_and_none(self):
        os.mknod("./tempTest")
        try:
            path = "./tempTest"

            chown(path, "nobody", "nogroup")
            assert SystemUser.load_from_file(path) == SystemUser.loads('nobody')
            assert (pwd.getpwuid(os.stat(path).st_uid).pw_name == "nobody")

            chown(path)
            assert (pwd.getpwuid(os.stat(path).st_uid).pw_name == "nobody")
        finally:
            os.remove("./tempTest")


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
