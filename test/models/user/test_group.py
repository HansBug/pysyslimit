import grp
import os

import pytest

from pysystem.models.user.group import SystemGroup


@pytest.mark.unittest
class TestSystemGroup:
    def test_group(self):
        group = SystemGroup()
        assert group.passwd == grp.getgrgid(os.getgid()).gr_passwd
        group = SystemGroup(name="root")
        assert str(group) == "root"
        assert repr(group) == r"<SystemGroup root, id: 0>"
        for _mem in grp.getgrgid(os.getgid()).gr_mem:
            flag = False
            for _user in group.mem:
                if _user.uid == _mem:
                    flag = True
            assert flag
        for _user in group.users + group.mem:
            flag = False
            for __user in group.full_members:
                if __user.uid == _user.uid:
                    flag = True
            assert flag
        current_group = group.current()
        no_group = group.nogroup()
        root_group = group.root()
        for _group in grp.getgrall():
            flag = False
            for __group in group.all():
                if _group.gr_gid == __group.gid:
                    flag = True
            assert flag
        assert len(grp.getgrall()) == len(group.all())
        os.mknod("./tempTest")
        assert group.load_from_file("./tempTest").gid == os.stat("./tempTest").st_gid
        os.remove("./tempTest")
        assert group.loads(root_group).name == "root"
        assert group.loads(0).gid == 0
        assert group.loads("root").name == "root"


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
