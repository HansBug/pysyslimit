import pytest

from pysystem.api.user.useradd import useradd, UseraddExecuteException
from pysystem.api.user.userdel import userdel, UserdelExecuteException


@pytest.mark.unittest
class TestApiUserAdd:
    def test_useradd_exception(self):
        try:
            useradd(name="newuser", uid=60000, primary_group=0, groups=[0,0,0], password="password",
                          system=True, comment="comment", user_group=True, no_user_group=True,
                          create_home=True, no_create_home=True, home_dir="./", base_dir="./",
                          shell="./", chroot_dir=True, selinux_user=True, extra_users=True, safe=False)
        except UseraddExecuteException as _e:
            return
        userdel(name="")
        assert False

    def test_useradd_safe(self):
        if not useradd(name="newuser2", safe=True):
            return
        if useradd(name="newuser2", safe=True):
            userdel(name="newuser2", safe=True)
            assert False

    def test_groupadd_normal(self):
        if not useradd("newuser3").name == "newuser3":
            userdel(name="newuser3", safe=True)
            assert False
        userdel(name="newuser3", safe=True)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
