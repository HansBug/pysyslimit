import pytest
import os
import pwd

from pysystem.models.user.user import SystemUser


@pytest.mark.unittest
class TestSystemUser:
    def test_1(self):
        user = SystemUser(name="root")
        assert user.name == "root"


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
