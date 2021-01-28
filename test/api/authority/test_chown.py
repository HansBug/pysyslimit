import os

import pwd
import pytest

from pysystem.api.authority.chown import chown


@pytest.mark.unittest
class TestApiAuthorityChown:
    def setup(self):
        os.mknod("./tempTest")

    def teardown(self):
        os.remove("./tempTest")

    def test_user_rootandnone(self):
        path = "./tempTest"
        chown(path, "root", "root")
        assert (pwd.getpwuid(os.stat(path).st_uid).pw_name == "root")
        chown(path)
        assert (pwd.getpwuid(os.stat(path).st_uid).pw_name == "root")


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
