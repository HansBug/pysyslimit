import os

import pytest

from pysyslimit.models.permission.full import FilePermission


@pytest.mark.unittest
class TestModelsPermissionFull:
    def test_full(self):
        fa = FilePermission.loads(0)
        assert fa.user.value == 0
        assert fa.group.value == 0
        assert fa.other.value == 0

        fa.user = 7
        fa.group = 3
        fa.other = 7
        assert fa.sign == "rwx-wxrwx"

        fa.sign = "------rwx"
        assert str(fa) == "------rwx"
        assert fa.oct_value == "007"
        assert repr(fa) == '<FilePermission permission: ------rwx>'

    def test_full_invalid(self):
        with pytest.raises(ValueError):
            FilePermission.load_by_sign('93485')
        with pytest.raises(TypeError):
            FilePermission.load_by_sign([])

        with pytest.raises(ValueError):
            FilePermission.load_by_value('9999')
        with pytest.raises(ValueError):
            FilePermission.load_by_value('999')
        with pytest.raises(ValueError):
            FilePermission.loads(3495809348)
        with pytest.raises(TypeError):
            FilePermission.load_by_value([])

        with pytest.raises(TypeError):
            FilePermission.loads([])

    def test_operator_full(self):
        fa1 = FilePermission.loads(0)
        fa1.sign = "------rwx"
        assert ("rw------x" | fa1).sign == "rw----rwx"
        assert ("rw------x" + fa1).sign == "rw----rwx"
        assert ("rw------x" & fa1).sign == "--------x"
        assert (fa1 & "rw------x").sign == "--------x"
        assert ("rw------x" - fa1).sign == "rw-------"

        p = FilePermission.loads('rw------x')
        p |= fa1
        assert p.sign == 'rw----rwx'
        p = FilePermission.loads('rw------x')
        p += fa1
        assert p.sign == 'rw----rwx'
        p = FilePermission.loads('rw------x')
        p &= fa1
        assert p.sign == '--------x'
        p = FilePermission.loads('rw------x')
        p -= fa1
        assert p.sign == 'rw-------'

    def test_eq(self):
        a = FilePermission.loads('754')
        assert a == a
        assert a == FilePermission.loads('754')
        assert a == FilePermission.loads('rwxr-xr--')
        assert not a == []

    def test_hash(self):
        d = {
            FilePermission.loads('754'): 1,
            FilePermission.loads(0): 3,
        }
        assert d[FilePermission.loads('rwxr-xr--')] == 1
        assert d[FilePermission.loads('---------')] == 3


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
