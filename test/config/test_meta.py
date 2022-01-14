import pytest

from pysyslimit.config.meta import __TITLE__


@pytest.mark.unittest
class TestConfigMeta:
    def test_meta(self):
        assert __TITLE__ == "pysyslimit"
