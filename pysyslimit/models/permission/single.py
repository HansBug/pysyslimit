import re


class _BaseVariables:
    _READ_WEIGHT = 1 << 2
    _WRITE_WEIGHT = 1 << 1
    _EXECUTE_WEIGHT = 1 << 0
    _SINGLE_WEIGHT = 1 << 3
    _FULL_WEIGHT = 1 << 9

    _SINGLE_MASK = _SINGLE_WEIGHT - 1
    _FULL_MASK = _FULL_WEIGHT - 1

    _SINGLE_DIGIT = r'\d'
    _FULL_DIGIT = r'{s}{s}{s}'.format(s=_SINGLE_DIGIT)

    _READ_SIGN = "r"
    _WRITE_SIGN = "w"
    _EXECUTE_SIGN = "x"
    _NONE_SIGN = "-"
    _SINGLE_SIGN = r'[{r}{n}][{w}{n}][{x}{n}]'.format(
        r=_READ_SIGN,
        w=_WRITE_SIGN,
        x=_EXECUTE_SIGN,
        n=_NONE_SIGN,
    )
    _FULL_SIGN = r'{s}{s}{s}'.format(s=_SINGLE_SIGN)


class FileSinglePermission(_BaseVariables):
    """
    Overview:
        Single permission of the files.
        With read(r), write(w) and execute(x).
    """

    def __init__(self, readable=False, writable=False, executable=False):
        """
        Overview:
            Constructor function.

        Arguments:
            - readable: Readable or not.
            - writable: Writable or not.
            - executable: Executable or not.
        """
        self.__readable = not not readable
        self.__writable = not not writable
        self.__executable = not not executable

    @property
    def readable(self):
        """
        Overview:
            Readable or not.
        """
        return self.__readable

    @readable.setter
    def readable(self, value):
        self.__readable = not not value

    @property
    def writable(self):
        """
        Overview:
            Writable or not.
        """
        return self.__writable

    @writable.setter
    def writable(self, value):
        self.__writable = not not value

    @property
    def executable(self):
        """
        Overview:
            Executable or not.
        """
        return self.__executable

    @executable.setter
    def executable(self, value):
        self.__executable = not not value

    @property
    def value(self) -> int:
        """
        Overview:
            Int value of current permission.
        """
        return sum([
            int(self.__readable) * self._READ_WEIGHT,
            int(self.__writable) * self._WRITE_WEIGHT,
            int(self.__executable) * self._EXECUTE_WEIGHT
        ])

    @value.setter
    def value(self, val):
        if isinstance(val, str):
            if not re.fullmatch(self._SINGLE_DIGIT, val):
                raise ValueError('Single digit expected but {actual} found.'.format(actual=repr(val)))
            val = int(val)

        if isinstance(val, int):
            if val >= self._SINGLE_WEIGHT:
                raise ValueError('Value from 0 to 7 expected but {actual} found.'.format(actual=repr(oct(val)[2:])))
        else:
            raise TypeError('Integer or integer-like string expected but {actual} found.'.format(actual=repr(val)))

        self.__readable = not not (val & self._READ_WEIGHT)
        self.__writable = not not (val & self._WRITE_WEIGHT)
        self.__executable = not not (val & self._EXECUTE_WEIGHT)

    def __int__(self):
        """
        Overview:
            Int format of this permission.
            The same as ``value``.
        """
        return self.value

    @property
    def sign(self):
        """
        Overview:
            Sign format of this permission.
            Such as ``rwx``.
        """
        return "%s%s%s" % (
            self._READ_SIGN if self.__readable else self._NONE_SIGN,
            self._WRITE_SIGN if self.__writable else self._NONE_SIGN,
            self._EXECUTE_SIGN if self.__executable else self._NONE_SIGN,
        )

    @sign.setter
    def sign(self, value):
        if isinstance(value, str):
            if re.fullmatch(r'[{r}{n}][{w}{n}][{x}{n}]'.format(
                    r=self._READ_SIGN,
                    w=self._WRITE_SIGN,
                    x=self._EXECUTE_SIGN,
                    n=self._NONE_SIGN,
            ), value):
                self.__readable = value[0] == self._READ_SIGN
                self.__writable = value[1] == self._WRITE_SIGN
                self.__executable = value[2] == self._EXECUTE_SIGN
            else:
                raise ValueError('Invalid single sign - {actual}.'.format(actual=repr(value)))
        else:
            raise TypeError('Str expected but {actual} found.'.format(actual=repr(type(value))))

    def __tuple(self):
        return self.__readable, self.__writable, self.__executable

    def __eq__(self, other):
        """
        Overview:
            Get equality of single permission.
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
            Get hash of single permission.
        """
        return hash(self.__tuple())

    def __str__(self):
        """
        Overview:
            String format of this permission.
            The same as ``sign``.
        """
        return self.sign

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
        elif isinstance(value, (int, str)):
            try:
                return cls.load_by_value(value)
            except (ValueError, TypeError):
                return cls.load_by_sign(value)
        else:
            raise TypeError('Int or str expected but {actual} found.'.format(actual=repr(type(value))))

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

    def __or__(self, other):
        """
        Overview:
            Merge permissions.
        """
        _other = self.loads(other)
        return self.__class__(
            readable=self.readable or _other.readable,
            writable=self.writable or _other.writable,
            executable=self.executable or _other.executable,
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
        self.readable = self.readable or _other.readable
        self.writable = self.writable or _other.writable
        self.executable = self.executable or _other.executable
        return self

    def __sub__(self, other):
        """
        Overview:
            Permission subtract.
        """
        _other = self.loads(other)
        return self.__class__(
            readable=self.readable and not _other.readable,
            writable=self.writable and not _other.writable,
            executable=self.executable and not _other.executable,
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
        self.readable = self.readable and not _other.readable
        self.writable = self.writable and not _other.writable
        self.executable = self.executable and not _other.executable
        return self

    def __and__(self, other):
        """
        Overview:
            Permission intersection.
        """
        _other = self.loads(other)
        return self.__class__(
            readable=self.readable and _other.readable,
            writable=self.writable and _other.writable,
            executable=self.executable and _other.executable,
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
        self.readable = self.readable and _other.readable
        self.writable = self.writable and _other.writable
        self.executable = self.executable and _other.executable
        return self
