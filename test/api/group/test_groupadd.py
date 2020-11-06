import pytest
import os
import pwd

from pysystem.api.group.groupadd import groupadd, GroupaddExecuteException
from pysystem.api.group.groupdel import groupdel, GroupdelExecuteException


@pytest.mark.unittest
class TestApiGroupAdd:
    def test_groupadd_exception(self):
        try:
            groupadd(name="newgroup", force=True, gid=600, non_unique=True,
                 password="password", system=True, chroot_dir="./",
                 extra_users=True, safe=False)
        except GroupaddExecuteException as _e:
            return
        groupdel(name="newgroup")
        assert False

    def test_groupadd_safe(self):
        if not groupadd(name="newgroup2", safe=True):
            return
        if groupadd(name="newgroup2", safe=True):
            groupdel(name="newgroup2", safe=True)
            assert False

    def test_groupadd_normal(self):
        if not groupadd("newgroup3").name == "newgroup3":
            groupdel(name="newgroup3", safe=True)
            assert False
        groupdel(name="newgroup3", safe=True)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
