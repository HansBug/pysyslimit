import os

import pytest

from pysyslimit.models.authority.full import FileAuthority


@pytest.mark.unittest
class TestModelsAuthorityFull:
    def test_full(self):
        fa = FileAuthority.loads(0)
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
        assert repr(fa) == '<FileAuthority authority: ------rwx>'

    def test_full_invalid(self):
        with pytest.raises(ValueError):
            FileAuthority.load_by_sign('93485')
        with pytest.raises(TypeError):
            FileAuthority.load_by_sign([])

        with pytest.raises(ValueError):
            FileAuthority.load_by_value('9999')
        with pytest.raises(ValueError):
            FileAuthority.load_by_value('999')
        with pytest.raises(ValueError):
            FileAuthority.loads(3495809348)
        with pytest.raises(TypeError):
            FileAuthority.load_by_value([])

        with pytest.raises(TypeError):
            FileAuthority.loads([])

    def test_operator_full(self):
        fa1 = FileAuthority.loads(0)
        fa1.sign = "------rwx"
        assert ("rw------x" | fa1).sign == "rw----rwx"
        assert ("rw------x" + fa1).sign == "rw----rwx"
        assert ("rw------x" & fa1).sign == "--------x"
        assert (fa1 & "rw------x").sign == "--------x"
        assert ("rw------x" - fa1).sign == "rw-------"

    def test_eq(self):
        a = FileAuthority.loads('754')
        assert a == a
        assert a == FileAuthority.loads('754')
        assert a == FileAuthority.loads('rwxr-xr--')
        assert not a == []

    def test_hash(self):
        d = {
            FileAuthority.loads('754'): 1,
            FileAuthority.loads(0): 3,
        }
        assert d[FileAuthority.loads('rwxr-xr--')] == 1
        assert d[FileAuthority.loads('---------')] == 3


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
