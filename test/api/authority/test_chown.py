import pytest
import os
import pwd

from pysystem.api.authority.chown import chown


@pytest.mark.unittest
class TestApiAuthorityChown:

    def setup(self):
        print("test api authority chown start--------")
        os.mknod("./tempTest")
    
    def teardown(self):
        print("end")
        os.remove("./tempTest")


    def test_user_none(self):
        path = "./tempTest"
        chown(path, "root", "root")
        assert(pwd.getpwuid(os.stat(path).st_uid).pw_name == "root")


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
