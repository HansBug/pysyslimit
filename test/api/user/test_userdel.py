import os

import pytest
import where

from pysyslimit.api import useradd, userdel, UserdelExecuteException


@pytest.mark.unittest
class TestApiUserDel:
    def test_userdel_exception(self):
        with pytest.raises(UserdelExecuteException) as excinfo:
            userdel(user_name="this_user_not_exist", force=True, remove_dir=True, chroot_dir="./", selinux_user=True,
                    safe=False)
        assert excinfo.type == UserdelExecuteException

    def test_userdel_safe(self):
        assert not userdel(user_name="this_user_not_exist", safe=True)

    def test_userdel_normal(self):
        try:
            useradd(user_name="this_user_not_exist", safe=True)
            assert userdel(user_name="this_user_not_exist", safe=True)
        finally:
            userdel('this_user_not_exist', safe=True)

    def test_userdel_invalid(self, mocker):
        mocker.patch.object(where, 'first', return_value=None)
        with pytest.raises(EnvironmentError):
            userdel('this_user_not_exist')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
