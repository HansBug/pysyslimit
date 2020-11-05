import pytest
import os
import grp
import pwd

from pysystem.models.user.user import SystemUser
from pysystem.models.user.group import SystemGroup


@pytest.mark.unittest
class TestSystemUser:
    def test_1(self):
        user = SystemUser(name="root")
        assert user.name == "root"
        user = SystemUser(uid=0)
        assert user.uid == 0
        user = SystemUser()
        assert user.uid == os.getuid()
        assert user.passwd == pwd.getpwuid(os.getuid()).pw_passwd
        assert user.gid == pwd.getpwuid(os.getuid()).pw_gid
        assert user.gecos == pwd.getpwuid(os.getuid()).pw_gecos
        assert user.dir == pwd.getpwuid(os.getuid()).pw_dir
        assert user.shell == pwd.getpwuid(os.getuid()).pw_shell
        assert SystemGroup(user.gid).name == user.primary_group.name
        assert SystemGroup(user.gid).gid == user.primary_group.gid
        _groups = user.groups
        for _group in _groups:
            flag = False
            for _user in _group.users:
                if _user.uid == user.uid:
                    flag = True
            assert flag
        for __group in grp.getgrall():
            _group = SystemGroup(__group.gr_gid)
            found = False
            for tGroup in _groups:
                if _group.gid == tGroup.gid:
                    found = True
            if found:
                continue
            flag = False
            for _user in _group.users:
                if _user.uid == user.uid:
                    flag = True
            assert flag == False

if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
