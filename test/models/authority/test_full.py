import pytest

from pysystem.models.authority.full import FileAuthority


@pytest.mark.unittest
class TestModelsAuthorityFull:
    def test_full(self):
        fa = FileAuthority.loads(0)
        assert fa.user.value == 0
        fa.user = 7
        assert fa.group.value == 0
        fa.group = 3
        assert fa.other.value == 0
        fa.other = 7
        assert fa.sign == "rwx-wxrwx"
        fa.sign = "rwx"
        assert str(fa) == "------rwx"
        assert fa.oct_value == "007"
        assert repr(fa) == '<FileAuthority authority: ------rwx>'
        noneValue = []
        assert not FileAuthority.loads(noneValue)

    def test_operator_full(self):
        fa1 = FileAuthority.loads(0)
        fa1.sign = "------rwx"
        assert ("rw------x" | fa1).sign == "rw----rwx"
        assert ("rw------x" + fa1).sign == "rw----rwx"
        assert ("rw------x" & fa1).sign == "--------x"
        assert (fa1 & "rw------x").sign == "--------x"
        assert ("rw------x" - fa1).sign == "rw-------"



if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
