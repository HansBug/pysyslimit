import pytest

from pysystem.api.group.groupdel import groupdel, GroupdelExecuteException
from pysystem.api.group.groupadd import groupadd, GroupaddExecuteException


@pytest.mark.unittest
class TestApiGroupDel:
    def test_groupdel_exception(self):
        try:
            groupdel(name="nonexistgroup", chroot_dir="./", force=True, safe=False)
        except GroupdelExecuteException as _e:
            return
        assert False

    def test_groupDel_safe(self):
        assert not groupdel(name="nonexistgroup", chroot_dir="./", force=True, safe=True)

    def test_groupDel_normal(self):
        groupadd(name="tempGroup", safe=True)
        assert groupdel(name="tempGroup", safe=True)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
