import pytest

from pysystem.configs.base import version


@pytest.mark.unittest
class TestConfigBase:
    def test_base(self):
        assert not not version


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
