import os
import shutil

import pytest

from pysystem.api.authority.chown import chown
from pysystem.models import SystemUser, SystemGroup


@pytest.mark.unittest
class TestApiAuthorityChown:
    def test_simple_file(self):
        os.mknod("./tempTest")
        try:
            path = "./tempTest"

            chown(path, "nobody", "nogroup")
            assert SystemUser.load_from_file(path) == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file(path) == SystemGroup.loads('nogroup')

            chown(path)
            assert SystemUser.load_from_file(path) == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file(path) == SystemGroup.loads('nogroup')

            chown(path, 'root')
            assert SystemUser.load_from_file(path) == SystemUser.loads('root')
            assert SystemGroup.load_from_file(path) == SystemGroup.loads('nogroup')

            chown(path, None, 'root')
            assert SystemUser.load_from_file(path) == SystemUser.loads('root')
            assert SystemGroup.load_from_file(path) == SystemGroup.loads('root')
        finally:
            os.remove("./tempTest")

    def test_recursive_dir(self):
        os.makedirs('./1/2/3')
        os.mknod('./1/2/3/file')
        try:
            chown('./1', 'nobody', 'nogroup')
            assert SystemUser.load_from_file('./1') == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file('./1') == SystemGroup.loads('nogroup')
            assert SystemUser.load_from_file('./1/2') == SystemUser.current()
            assert SystemGroup.load_from_file('./1/2') == SystemGroup.current()
            assert SystemUser.load_from_file('./1/2/3') == SystemUser.current()
            assert SystemGroup.load_from_file('./1/2/3') == SystemGroup.current()
            assert SystemUser.load_from_file('./1/2/3/file') == SystemUser.current()
            assert SystemGroup.load_from_file('./1/2/3/file') == SystemGroup.current()

            chown('./1', 'nobody', 'nogroup', recursive=True)
            assert SystemUser.load_from_file('./1') == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file('./1') == SystemGroup.loads('nogroup')
            assert SystemUser.load_from_file('./1/2') == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file('./1/2') == SystemGroup.loads('nogroup')
            assert SystemUser.load_from_file('./1/2/3') == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file('./1/2/3') == SystemGroup.loads('nogroup')
            assert SystemUser.load_from_file('./1/2/3/file') == SystemUser.loads('nobody')
            assert SystemGroup.load_from_file('./1/2/3/file') == SystemGroup.loads('nogroup')
        finally:
            shutil.rmtree('./1', ignore_errors=True)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
