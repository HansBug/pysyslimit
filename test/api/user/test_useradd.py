import os

import pytest
import where

from pysystem.api import useradd, UseraddExecuteException, userdel


@pytest.mark.unittest
class TestApiUserAdd:
    def test_useradd_exception(self):
        try:
            with pytest.raises(UseraddExecuteException) as excinfo:
                useradd(user_name="newuser", uid=60000, primary_group="0", groups=[0, 0, 0], password="password",
                        system=True, comment="comment", user_group=True, no_user_group=True,
                        create_home=True, no_create_home=True, home_dir="./", base_dir="./",
                        shell="./", chroot_dir=True, selinux_user=True, extra_users=True, safe=False)
            assert excinfo.type == UseraddExecuteException
        finally:
            userdel('newuser', safe=True)

    def test_useradd_safe(self):
        try:
            if useradd(user_name="newuser2", safe=True):
                if useradd(user_name="newuser2", safe=True):
                    pytest.fail("Should not reach here")
            else:
                pytest.fail("Should not reach here")
        finally:
            userdel('newuser2', safe=True)

    def test_useradd_normal(self):
        try:
            if not useradd("newuser3").name == "newuser3":
                pytest.fail("Should not reach here")
        finally:
            userdel('newuser3', safe=True)

    def test_useradd_invalid(self, mocker):
        mocker.patch.object(where, 'first', return_value=None)
        with pytest.raises(EnvironmentError):
            useradd('newuser4')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
