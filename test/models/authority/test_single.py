import os

import pytest

from pysystem.models.authority.single import *


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


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
