import os

import pytest

from pysyslimit.models.permission.single import *


@pytest.mark.unittest
class TestModelsPermissionSingle:
    def test_single(self):
        single = FileSinglePermission.loads(0)
        single.readable = 1
        single.writable = True
        single.executable = 0
        assert int(single) == 6
        assert str(single) == "rw-"
        assert repr(single) == "<FileSinglePermission permission: rw->"

    def test_single_2(self):
        single = FileSinglePermission.loads("rw-")
        assert int(single) == 6
        assert str(single + "r-x") == "rwx"
        assert str("r-x" + single) == "rwx"
        assert str("r-x" | single) == "rwx"
        assert str("r-x" - single) == "--x"
        assert str("r-x" & single) == "r--"

        p = FileSinglePermission.loads('r-x')
        p += single
        assert str(p) == 'rwx'
        p = FileSinglePermission.loads('r-x')
        p |= single
        assert str(p) == 'rwx'
        p = FileSinglePermission.loads('r-x')
        p -= single
        assert str(p) == '--x'
        p = FileSinglePermission.loads('r-x')
        p &= single
        assert str(p) == 'r--'

    def test_single_invalid(self):
        with pytest.raises(TypeError):
            FileSinglePermission.loads(None)
        with pytest.raises(ValueError):
            FileSinglePermission.loads('siodf')
        with pytest.raises(ValueError):
            FileSinglePermission.loads('xrw')
        with pytest.raises(ValueError):
            FileSinglePermission.loads('8')

        f = FileSinglePermission.loads(7)
        with pytest.raises(TypeError):
            f.sign = None
        with pytest.raises(TypeError):
            f.value = None

    def test_eq(self):
        a = FileSinglePermission.loads('rw-')
        assert a == a
        assert a == FileSinglePermission.loads('rw-')
        assert a == FileSinglePermission.loads(6)
        assert not a == []

    def test_hash(self):
        d = {
            FileSinglePermission.loads('rw-'): 1,
            FileSinglePermission.loads(5): 2,
        }
        assert d[FileSinglePermission.loads(6)] == 1
        assert d[FileSinglePermission.loads('r-x')] == 2


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
