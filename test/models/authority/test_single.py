import os

import pytest

from pysyslimit.models.authority.single import *


@pytest.mark.unittest
class TestModelsAuthoritySingle:
    def test_single(self):
        single = FileSingleAuthority.loads(0)
        single.readable = 1
        single.writable = True
        single.executable = 0
        assert int(single) == 6
        assert str(single) == "rw-"
        assert repr(single) == "<FileSingleAuthority authority: rw->"

    def test_single_2(self):
        single = FileSingleAuthority.loads("rw-")
        assert int(single) == 6
        assert str(single + "r-x") == "rwx"
        assert str("r-x" + single) == "rwx"
        assert str("r-x" | single) == "rwx"
        assert str("r-x" - single) == "--x"
        assert str("r-x" & single) == "r--"

    def test_single_invalid(self):
        with pytest.raises(TypeError):
            FileSingleAuthority.loads(None)
        with pytest.raises(ValueError):
            FileSingleAuthority.loads('siodf')
        with pytest.raises(ValueError):
            FileSingleAuthority.loads('xrw')
        with pytest.raises(ValueError):
            FileSingleAuthority.loads('8')

        f = FileSingleAuthority.loads(7)
        with pytest.raises(TypeError):
            f.sign = None
        with pytest.raises(TypeError):
            f.value = None

    def test_eq(self):
        a = FileSingleAuthority.loads('rw-')
        assert a == a
        assert a == FileSingleAuthority.loads('rw-')
        assert a == FileSingleAuthority.loads(6)
        assert not a == []

    def test_hash(self):
        d = {
            FileSingleAuthority.loads('rw-'): 1,
            FileSingleAuthority.loads(5): 2,
        }
        assert d[FileSingleAuthority.loads(6)] == 1
        assert d[FileSingleAuthority.loads('r-x')] == 2


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
