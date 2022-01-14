import os
import re

from .single import FileSinglePermission, _BaseVariables


class FileUserPermission(FileSinglePermission):
    """
    Overview:
        Single permission of the user part of a file.
        Inherited from :class:`pysyslimit.models.permission.single.FileSinglePermission`.
        With read(r), write(w) and execute(x).
    """
    pass


class FileGroupPermission(FileSinglePermission):
    """
    Overview:
        Single permission of the group part of a file.
        Inherited from :class:`pysyslimit.models.permission.single.FileSinglePermission`.
        With read(r), write(w) and execute(x).
    """
    pass


class FileOtherPermission(FileSinglePermission):
    """
    Overview:
        Single permission of the other part of a file.
        Inherited from :class:`pysyslimit.models.permission.single.FileSinglePermission`.
        With read(r), write(w) and execute(x).
    """
    pass


class FilePermission(_BaseVariables):
    """
    Overview:
        Full file permission class. 
    """

    def __init__(self, user_permission=None, group_permission=None, other_permission=None):
        """
        Overview:
            Constructor function.

        Arguments:
            - user_permission: User permission.
            - group_permission: User group permission.
            - other_permission: Other permission.
        """
        self.__user_permission = FileUserPermission.loads(user_permission or FileUserPermission())
        self.__group_permission = FileGroupPermission.loads(group_permission or FileGroupPermission())
        self.__other_permission = FileOtherPermission.loads(other_permission or FileOtherPermission())

    @property
    def user(self):
        """
        Overview:
            User permission.
        """
        return self.__user_permission

    @user.setter
    def user(self, value):
        self.__user_permission = FileUserPermission.loads(value)

    @property
    def group(self):
        """
        Overview:
            User group permission.
        """
        return self.__group_permission

    @group.setter
    def group(self, value):
        self.__group_permission = FileGroupPermission.loads(value)

    @property
    def other(self):
        """
        Overview:
            Other permission.
        """
        return self.__other_permission

    @other.setter
    def other(self, value):
        self.__other_permission = FileOtherPermission.loads(value)

    @property
    def sign(self):
        """
        Overview:
            Sign format of this permission.
            Such as ``rwxrwxrwx``.
        """
        return "%s%s%s" % (
            self.__user_permission.sign,
            self.__group_permission.sign,
            self.__other_permission.sign,
        )

    @sign.setter
    def sign(self, value):
        if isinstance(value, str):
            if re.fullmatch(self._FULL_SIGN, value):
                self.__user_permission.sign = value[0:3]
                self.__group_permission.sign = value[3:6]
                self.__other_permission.sign = value[6:9]
            else:
                raise ValueError('Invalid single sign - {actual}.'.format(actual=repr(value)))
        else:
            raise TypeError('Str expected but {actual} found.'.format(actual=repr(type(value))))

    def __str__(self):
        """
        Overview:
            String format of this permission.
            The same as ``sign``.
        """
        return self.sign

    @property
    def value(self):
        """
        Overview:
            Int value of current permission.
        """
        return sum([
            self.__user_permission.value * 64,
            self.__group_permission.value * 8,
            self.__other_permission.value * 1,
        ])

    @value.setter
    def value(self, val):
        if isinstance(val, str):
            if not re.fullmatch(self._FULL_DIGIT, val):
                raise ValueError('3-length digit expected but {actual} found.'.format(actual=repr(val)))
            val = int(val, 8)

        if isinstance(val, int):
            if val >= self._FULL_WEIGHT:
                raise ValueError('Value from 000 to 777 expected but {actual} found.'.format(actual=repr(oct(val)[2:])))
        else:
            raise TypeError('Integer or integer-like string expected but {actual} found.'.format(actual=repr(val)))

        self.__user_permission.value = int(val / 64) & 7
        self.__group_permission.value = int(val / 8) & 7
        self.__other_permission.value = int(val / 1) & 7

    def __int__(self):
        """
        Overview:
            Int format of this permission.
            The same as ``value``.
        """
        return self.value

    @property
    def oct_value(self):
        """
        Overview:
            Octal tnt value of current permission.
            Such as ``777``.
        """
        _value = oct(self.value)[2:]
        _value = "0" * (3 - len(_value)) + _value
        return _value

    @oct_value.setter
    def oct_value(self, value):
        # noinspection PyAttributeOutsideInit
        self.value = int(str(value), 8)

    def __tuple(self):
        return self.__user_permission, self.__group_permission, self.__other_permission

    def __eq__(self, other):
        """
        Overview:
            Get equality of full permission.
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
            Get hash of full permission.
        """
        return hash(self.__tuple())

    def __repr__(self):
        """
        Overview:
            String representation format of this permission.
        """
        return '<%s permission: %s>' % (
            self.__class__.__name__,
            self.sign
        )

    @classmethod
    def load_by_value(cls, value):
        """
        Overview:
            Load permission by int value.

        Arguments:
            - value: Int value of permission.

        Returns:
            - permission: Loaded permission object.
        """
        _instance = cls()
        _instance.value = value
        return _instance

    @classmethod
    def load_by_sign(cls, sign):
        """
        Overview:
            Load permission by string sign.

        Arguments:
            - value: String sign of permission.

        Returns:
            - permission: Loaded permission object.
        """
        _instance = cls()
        _instance.sign = sign
        return _instance

    @classmethod
    def load_by_oct_value(cls, oct_value):
        """
        Overview:
            Load permission by octal value.

        Arguments:
            - value: Octal value of permission.

        Returns:
            - permission: Loaded permission object.
        """
        _instance = cls()
        _instance.oct_value = oct_value
        return _instance

    @classmethod
    def loads(cls, value):
        """
        Overview:
            Load permission by any types of value.

        Arguments:
            - value: Any types of value of permission.

        Returns:
            - permission: Loaded permission object.
        """
        if isinstance(value, cls):
            return value
        elif isinstance(value, int):
            return cls.load_by_value(value)
        elif isinstance(value, str):
            if re.fullmatch(r"\d+", value):
                return cls.load_by_oct_value(value)
            else:
                return cls.load_by_sign(value)
        else:
            raise TypeError('Int or str expected but {actual} found.'.format(actual=repr(type(value))))

    @classmethod
    def load_from_file(cls, filename):
        """
        Overview:
            Get file's permission.

        Arguments:
            - filename: Name of the file.

        Returns:
            - permission: Permission object.
        """
        return cls.load_by_value(os.stat(filename).st_mode & cls._FULL_MASK)

    def __or__(self, other):
        """
        Overview:
            Merge permissions.
        """
        _other = self.loads(other)
        return self.__class__(
            user_permission=self.__user_permission | _other.__user_permission,
            group_permission=self.__group_permission | _other.__group_permission,
            other_permission=self.__other_permission | _other.__other_permission,
        )

    def __ror__(self, other):
        """
        Overview:
            Merge permissions, right version.
        """
        return self | other

    def __ior__(self, other):
        """
        Overview:
            Merge permissions, self version.
        """
        _other = self.loads(other)
        self.__user_permission |= _other.__user_permission
        self.__group_permission |= _other.__group_permission
        self.__other_permission |= _other.__other_permission
        return self

    def __add__(self, other):
        """
        Overview:
            Merge permissions, the same as ``|``.
        """
        return self | other

    def __radd__(self, other):
        """
        Overview:
            Merge permissions, right version.
        """
        return self + other

    def __iadd__(self, other):
        """
        Overview:
            Merge permissions, self version.
        """
        self |= other
        return self

    def __and__(self, other):
        """
        Overview:
            Permission intersection.
        """
        _other = self.loads(other)
        return self.__class__(
            user_permission=self.__user_permission & _other.__user_permission,
            group_permission=self.__group_permission & _other.__group_permission,
            other_permission=self.__other_permission & _other.__other_permission,
        )

    def __rand__(self, other):
        """
        Overview:
            Permission intersection, right version.
        """
        return self & other

    def __iand__(self, other):
        """
        Overview:
            Permission intersection, self version.
        """
        _other = self.loads(other)
        self.__user_permission &= _other.__user_permission
        self.__group_permission &= _other.__group_permission
        self.__other_permission &= _other.__other_permission
        return self

    def __sub__(self, other):
        """
        Overview:
            Permission subtract.
        """
        _other = self.loads(other)
        return self.__class__(
            user_permission=self.__user_permission - _other.__user_permission,
            group_permission=self.__group_permission - _other.__group_permission,
            other_permission=self.__other_permission - _other.__other_permission,
        )

    def __rsub__(self, other):
        """
        Overview:
            Permission subtract, right version.
        """
        return self.loads(other) - self

    def __isub__(self, other):
        """
        Overview:
            Permission subtract, self version.
        """
        _other = self.loads(other)
        self.__user_permission -= _other.__user_permission
        self.__group_permission -= _other.__group_permission
        self.__other_permission -= _other.__other_permission
        return self
