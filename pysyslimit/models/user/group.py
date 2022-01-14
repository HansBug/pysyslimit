import grp
import os


# noinspection PyMethodMayBeStatic
class SystemGroupAttaches:
    def groups(self):
        return [SystemGroup.loads(item) for item in os.getgroups()]

    def append(self, *args):
        os.setgroups(list(set(os.getgroups() + [SystemGroup.loads(item).gid for item in args])))

    def clear(self):
        os.setgroups([])

    def reset(self, *args):
        os.setgroups(list(set([SystemGroup.loads(item).gid for item in args])))


class SystemGroup:
    """
    Overview:
        System group class.
    """
    __NOGROUP = "nogroup"
    __ROOT = "root"

    def __init__(self, gid=None, name=None):
        """
        Overview:
            Constructor function.

        Arguments:
            - gid: Group id.
            - name: Group name.
        """
        if gid is not None:
            self.__object = grp.getgrgid(gid)
        elif name is not None:
            self.__object = grp.getgrnam(name)
        else:
            self.__object = grp.getgrgid(os.getgid())

    @property
    def name(self):
        """
        Overview:
            Group's name
        """
        return self.__object.gr_name

    @property
    def passwd(self):
        """
        Overview:
            Group's passwd
        """
        return self.__object.gr_passwd

    @property
    def gid(self):
        """
        Overview:
            Group's gid
        """
        return self.__object.gr_gid

    @property
    def mem(self):
        """
        Overview:
            Group's mem
        """
        return self.__object.gr_mem

    def apply(self):
        """
        Overview:
            Apply group's ownership to current env.
        """
        os.setgid(self.gid)

    def __tuple(self):
        return self.name, self.gid

    def __eq__(self, other):
        """
        Overview:
            Compare groups
        """
        if other is self:
            return True
        elif isinstance(other, self.__class__):
            return self.__tuple() == other.__tuple()
        else:
            return False

    def __hash__(self):
        """
        Overview:
            Get hash of group.
        """
        return hash(self.__tuple())

    def __str__(self):
        """
        Overview:
            String format.
        """
        return self.name

    def __repr__(self):
        """
        Overview:
            Representation format.
        """
        return r'<%s %s, id: %s>' % (
            type(self).__name__,
            self.name,
            self.gid
        )

    @property
    def users(self):
        """
        Overviews:
            Get all the users which primary group is this group.
        """
        from .user import SystemUser
        return [_user for _user in SystemUser.all() if _user.gid == self.gid]

    @property
    def members(self):
        """
        Overview:
            Get all the users with this group.
        """
        from .user import SystemUser
        return [SystemUser.loads(_member) for _member in self.mem]

    @property
    def full_members(self):
        """
        Overviews:
            Get all the users in ``members`` and ``users``.
        """
        from .user import SystemUser
        _ids = sorted(list(set([_item.uid for _item in (self.users + self.members)])))
        return [SystemUser(uid=_id) for _id in _ids]

    @classmethod
    def current(cls):
        """
        Overview:
            Get current group.
        """
        return cls()

    @classmethod
    def current_attaches(cls) -> SystemGroupAttaches:
        return SystemGroupAttaches()

    @classmethod
    def root(cls):
        """
        Overview:
            Get root group.
        """
        return cls(name=cls.__ROOT)

    @classmethod
    def nogroup(cls):
        """
        Overview:
            Get nobody group.
        """
        return cls(name=cls.__NOGROUP)

    @classmethod
    def all(cls):
        """
        Overview:
            Get all groups.
        """
        return [cls(gid=_group.gr_gid) for _group in grp.getgrall()]

    @classmethod
    def load_from_file(cls, filename):
        """
        Overview:
            Get the ownership of a file.

        Arguments:
            - filename: File's name.

        Returns:
            - ownership: File's group.
        """
        return cls(gid=os.stat(filename).st_gid)

    @classmethod
    def loads(cls, value):
        """
        Overview:
            Load group from any types of value.

        Arguments:
            - value: Any types of value.

        Returns:
            - group: Loaded group object.
        """
        if isinstance(value, int):
            return cls(gid=value)
        elif isinstance(value, cls):
            return value
        else:
            return cls(name=str(value))
