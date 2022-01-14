import grp
import os
import pwd

import pytest

from pysyslimit.models.user.group import SystemGroup
from pysyslimit.models.user.user import SystemUser


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestSystemUser:
    def test_user(self):
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
        assert user.primary_group.gid == os.getgid()
        assert str(user) == "root"
        assert repr(user) == r"<SystemUser root, id: 0>"
        current_user = user.current()
        assert current_user
        root_user = user.root()
        assert root_user
        nobody_user = user.nobody()
        assert nobody_user
        for _user in pwd.getpwall():
            flag = False
            for __user in user.all():
                if _user.pw_uid == __user.uid:
                    flag = True
            assert flag
        assert len(pwd.getpwall()) == len(user.all())

        os.mknod("./tempTest")
        try:
            assert user.load_from_file("./tempTest").uid == os.stat("./tempTest").st_uid
        finally:
            os.remove("./tempTest")
        assert user.loads(root_user).name == "root"
        assert user.loads(0).uid == 0
        assert user.loads("root").name == "root"

    def test_eq(self):
        g = SystemUser.loads('nobody')
        assert g == g
        assert g == SystemUser.loads('nobody')
        assert not g == SystemUser.loads('root')
        assert not g == []

    def test_hash(self):
        d = {
            SystemUser.loads('nobody'): 1,
            SystemUser.loads('root'): 2,
        }

        assert d[SystemUser.loads('nobody')] == 1
        assert d[SystemUser.loads('root')] == 2
