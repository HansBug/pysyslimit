import os
import pytest

from pysystem.configs.meta import __TITLE__


@pytest.mark.unittest
class TestConfigMeta:
    def test_meta(self):
        assert __TITLE__ == "pysystem"


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
