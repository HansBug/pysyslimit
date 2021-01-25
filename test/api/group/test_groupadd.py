import os
import pytest

from pysystem.api.group.groupadd import groupadd, GroupaddExecuteException
from pysystem.api.group.groupdel import groupdel


@pytest.mark.unittest
class TestApiGroupAdd:
    def test_groupadd_exception(self):
        with pytest.raises(GroupaddExecuteException) as excinfo:
            groupadd(name="newgroup", force=True, gid=600, non_unique=True,
                     password="password", system=True, chroot_dir="./",
                     extra_users=True, safe=False)
        groupdel(name="newgroup")
        assert excinfo.type == GroupaddExecuteException

    def test_groupadd_safe(self):
        if groupadd(name="newgroup2", safe=True):
            if groupadd(name="newgroup2", safe=True):
                groupdel(name="newgroup2", safe=True)
                pytest.fail("", False)

    def test_groupadd_normal(self):
        if not groupadd("newgroup3").name == "newgroup3":
            groupdel(name="newgroup3", safe=True)
            pytest.fail("", False)
        groupdel(name="newgroup3", safe=True)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
