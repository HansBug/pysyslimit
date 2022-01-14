import pytest
import where

from pysyslimit.api import groupadd, groupdel, GroupdelExecuteException


@pytest.mark.unittest
class TestApiGroupDel:
    def test_groupdel_exception(self):
        try:
            if groupadd(group_name="nonexistgroup", safe=True):
                with pytest.raises(GroupdelExecuteException) as excinfo:
                    groupdel(group_name="nonexistgroup", chroot_dir="./", force=True, safe=False)
                assert excinfo.type == GroupdelExecuteException
            else:
                pytest.fail('Should not reach here.')
        finally:
            groupdel('nonexistgroup', safe=True)

    def test_groupdel_safe(self):
        assert not groupdel(group_name="nonexistgroup", chroot_dir="./", force=True, safe=True)

    def test_groupdel_normal(self):
        try:
            groupadd(group_name="tempGroup", safe=True)
            assert groupdel(group_name="tempGroup", safe=True)
        finally:
            groupdel('tempGroup', safe=True)

    def test_groupdel_invalid(self, mocker):
        mocker.patch.object(where, 'first', return_value=None)
        with pytest.raises(EnvironmentError):
            groupdel('tempGroup')
