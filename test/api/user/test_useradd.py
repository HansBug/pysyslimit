import pytest

from pysystem.api.user.useradd import useradd, UseraddExecuteException
from pysystem.api.user.userdel import userdel, UserdelExecuteException


@pytest.mark.unittest
class TestApiUserAdd:
    def test_useradd_exception(self):
        with pytest.raises(UseraddExecuteException) as excinfo:
            useradd(name="newuser", uid=60000, primary_group="0", groups=[0,0,0], password="password",
                          system=True, comment="comment", user_group=True, no_user_group=True,
                          create_home=True, no_create_home=True, home_dir="./", base_dir="./",
                          shell="./", chroot_dir=True, selinux_user=True, extra_users=True, safe=False)
        assert excinfo.type == UseraddExecuteException

    def test_useradd_safe(self):
        if useradd(name="newuser2", safe=True):
            if useradd(name="newuser2", safe=True):
                pytest.fail("", False)

    def test_groupadd_normal(self):
        if not useradd("newuser3").name == "newuser3":
            pytest.fail("", False)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
