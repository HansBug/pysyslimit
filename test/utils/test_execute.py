import pytest

from pysyslimit.utils.execute import *


@pytest.mark.unittest
class TestUtilExecute:
    def test_execute(self):
        temp = ExecuteException("return_code", "stdout", "stderr")
        assert temp.return_code == "return_code"
        assert temp.stdout == "stdout"
        assert temp.stderr == "stderr"

    def test_execute_title(self):
        temp = ExecuteException("return_code", None, None)
        assert not temp.title
