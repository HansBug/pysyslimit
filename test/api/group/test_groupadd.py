import os

import pytest
import where

from pysystem.api import groupadd, GroupaddExecuteException, groupdel


@pytest.mark.unittest
class TestApiGroupAdd:
    def test_groupadd_exception(self):
        try:
            with pytest.raises(GroupaddExecuteException) as excinfo:
                groupadd(group_name="newgroup", force=True, gid=600, non_unique=True,
                         password="password", system=True, chroot_dir="./",
                         extra_users=True, safe=False)
            assert excinfo.type == GroupaddExecuteException
        finally:
            groupdel('newgroup', safe=True)

    def test_groupadd_safe(self):
        try:
            if groupadd(group_name="newgroup2", safe=True):
                if groupadd(group_name="newgroup2", safe=True):
                    pytest.fail("Should not reach here")
            else:
                pytest.fail("Should not reach here")
        finally:
            groupdel('newgroup2', safe=True)

    def test_groupadd_normal(self):
        try:
            if not groupadd("newgroup3").name == "newgroup3":
                pytest.fail("Should not reach here")
        finally:
            groupdel('newgroup3', safe=True)

    def test_groupadd_invalid(self, mocker):
        mocker.patch.object(where, 'first', return_value=None)
        with pytest.raises(EnvironmentError):
            groupadd('newgroup4')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
