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

        user.apply()
        assert os.getuid() == user.uid
        assert user.primary_group.gid in os.getgroups()
        assert str(user) == "root"
        assert repr(user) == r"<SystemUser root, id: 0>"
        current_user = user.current
        root_user = user.root
        nobody_user = user.nobody
        for _user in pwd.getpwall():
            flag = False
            for __user in user.all():
                if _user.pw_uid == __user.uid:
                    flag = True
            assert flag
        assert len(pwd.getpwall()) == len(user.all())
        os.mknod("./tempTest")
        assert user.load_from_file("./tempTest").uid == os.stat("./tempTest").st_uid
        os.remove("./tempTest")
        assert user.loads(root_user).name == "root"
        assert user.loads(0).uid == 0
        assert user.loads("root").name == "root"


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
