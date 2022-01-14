import os

import pwd


class SystemUser(object):
    """
    Overview:
        System user's class.
    """
    __NOBODY = "nobody"
    __ROOT = "root"

    def __init__(self, uid=None, name=None):
        """
        Overview:
            Constructor function.
        Arguments:
            - uid: User id
            - name: Username
        """
        if uid is not None:
            self.__object = pwd.getpwuid(uid)
        elif name is not None:
            self.__object = pwd.getpwnam(name)
        else:
            self.__object = pwd.getpwuid(os.getuid())

    @property
    def name(self):
        """
        Overview:
            User's name,
        """
        return self.__object.pw_name

    @property
    def passwd(self):
        """
        Overview:
           User's passwd
        """
        return self.__object.pw_passwd

    @property
    def uid(self):
        """
        Overview:
           User's uid
        """
        return self.__object.pw_uid

    @property
    def gid(self):
        """
        Overview:
           User's gid
        """
        return self.__object.pw_gid

    @property
    def gecos(self):
        """
        Overview:
           User's gecos
        """
        return self.__object.pw_gecos

    @property
    def dir(self):
        """
        Overview:
           User's dir
        """
        return self.__object.pw_dir

    @property
    def shell(self):
        """
        Overview:
           User's shell
        """
        return self.__object.pw_shell

    @property
    def primary_group(self):
        """
        Overview:
           User's primary group
        """
        from .group import SystemGroup
        return SystemGroup(gid=self.gid)

    @property
    def groups(self):
        """
        Overview:
           User's groups
        """
        from .group import SystemGroup
        _result = []
        for _group in SystemGroup.all():
            _ok = False
            for _user in _group.users:
                if _user.uid == self.uid:
                    _ok = True
                    break
            if _ok:
                _result += [_group]
        return _result

    def apply(self, include_group=True):
        """
        Overview:
            Apply user's ownership to current env.

        Arguments:
            - include_group: Apply group at the same time or not.
        """
        if include_group:
            self.primary_group.apply()
        os.setuid(self.uid)

    def __tuple(self):
        return self.name, self.uid

    def __eq__(self, other):
        """
        Overview:
            Compare users
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
            Get hash of user.
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
            self.uid
        )

    @classmethod
    def current(cls):
        """
        Overview:
            Get current user.
        """
        return cls()

    @classmethod
    def root(cls):
        """
        Overview:
            Get root user.
        """
        return cls(name=cls.__ROOT)

    @classmethod
    def nobody(cls):
        """
        Overview:
            Get nobody user.
        """
        return cls(name=cls.__NOBODY)

    @classmethod
    def all(cls):
        """
        Overview:
            Get all users.
        """
        return [cls(uid=_user.pw_uid) for _user in pwd.getpwall()]

    @classmethod
    def load_from_file(cls, filename):
        """
        Overview:
            Get the ownership of a file.

        Arguments:
            - filename: File's name.

        Returns:
            - ownership: File's user.
        """
        return cls(uid=os.stat(filename).st_uid)

    @classmethod
    def loads(cls, value):
        """
        Overview:
            Load user from any types of value.

        Arguments:
            - value: Any types of value.

        Returns:
            - user: Loaded user object.
        """
        if isinstance(value, int):
            return cls(uid=value)
        elif isinstance(value, cls):
            return value
        else:
            return cls(name=str(value))
