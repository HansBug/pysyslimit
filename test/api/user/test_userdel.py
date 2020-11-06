import pytest

from pysystem.api.user.useradd import useradd, UseraddExecuteException
from pysystem.api.user.userdel import userdel, UserdelExecuteException


@pytest.mark.unittest
class TestApiUserDel:
    def test_userdel_exception(self):
        try:
            userdel(name="this_user_not_exist", force=True, remove_dir=True, chroot_dir="./", selinux_user=True, safe=False)
        except UserdelExecuteException as _e:
            return
        assert False

    def test_userdel_safe(self):
        assert not userdel(name="this_user_not_exist", safe=True)

    def test_groupadd_normal(self):
        useradd(name="this_user_not_exist", safe=True)
        assert userdel(name="this_user_not_exist", safe=True)

if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
