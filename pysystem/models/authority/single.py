import re


class FileSingleAuthority(object):
    """
    单个权限类
    """
    __read_weight = 4
    __write_weight = 2
    __execute_weight = 1
    __read_sign = "r"
    __write_sign = "w"
    __execute_sign = "x"
    __none_sign = "-"

    def __init__(self, readable=False, writable=False, executable=False):
        """
        构造函数
        :param readable: 是否可读
        :param writable: 是否可写
        :param executable: 是否可执行
        """
        self.__readable = not not readable
        self.__writable = not not writable
        self.__executable = not not executable

    @property
    def readable(self):
        """
        获取可读性
        :return: 可读性
        """
        return self.__readable

    @readable.setter
    def readable(self, value):
        """
        设置可读性
        :param value: 可读性
        """
        self.__readable = not not value

    @property
    def writable(self):
        """
        获取可写性
        :return: 可写性
        """
        return self.__writable

    @writable.setter
    def writable(self, value):
        """
        设置可写性
        :param value: 可写性
        """
        self.__writable = not not value

    @property
    def executable(self):
        """
        获取可执行性
        :return: 可执行性
        """
        return self.__executable

    @executable.setter
    def executable(self, value):
        """
        设置可执行性
        :param value: 可执行性
        """
        self.__executable = not not value

    @property
    def value(self):
        """
        获取权限权值
        :return: 权限权值
        """
        return sum([
            int(self.__readable) * self.__read_weight,
            int(self.__writable) * self.__write_weight,
            int(self.__executable) * self.__execute_weight
        ])

    @value.setter
    def value(self, val):
        """
        设置权限权值
        :param val: 权限权值
        """
        if isinstance(val, str):
            if not re.fullmatch(r'\d', val):
                raise ValueError('Single digit expected but {actual} found.'.format(actual=repr(val)))
            val = int(val)

        if isinstance(val, int):
            if len(oct(val)) != 3:
                raise ValueError('Value from 0 to 7 expected but {actual} found.'.format(actual=repr(val)))
        else:
            raise TypeError('Integer or integer-like string expected but {actual} found.'.format(actual=repr(val)))

        self.__readable = not not (val & self.__read_weight)
        self.__writable = not not (val & self.__write_weight)
        self.__executable = not not (val & self.__execute_weight)

    def __int__(self):
        """
        获取数字格式（即权限权值）
        :return: 数字格式
        """
        return self.value

    @property
    def sign(self):
        """
        获取标记格式（rwx格式）
        :return: 标记格式
        """
        return "%s%s%s" % (
            self.__read_sign if self.__readable else self.__none_sign,
            self.__write_sign if self.__writable else self.__none_sign,
            self.__execute_sign if self.__executable else self.__none_sign,
        )

    @sign.setter
    def sign(self, value):
        """
        设置标记格式
        :param value: 标记格式
        """
        if isinstance(value, str):
            if re.fullmatch(r'[r-][w-][x-]', value):
                self.__readable = value[0] == self.__read_sign
                self.__writable = value[1] == self.__write_sign
                self.__executable = value[2] == self.__execute_sign
            else:
                raise ValueError('Invalid single sign - {actual}.'.format(actual=repr(value)))
        else:
            raise TypeError('Str expected but {actual} found.'.format(actual=repr(type(value))))

    def __str__(self):
        """
        获取字符串格式（即标记格式）
        :return: 字符串格式
        """
        return self.sign

    def __repr__(self):
        """
        获取表达式格式
        :return: 表达式格式
        """
        return '<%s authority: %s>' % (
            self.__class__.__name__,
            self.sign
        )

    @classmethod
    def load_by_value(cls, value):
        """
        根据数值加载对象
        :param value: 数值(0-7)
        :return: 加载对象
        """
        _instance = cls()
        _instance.value = value
        return _instance

    @classmethod
    def load_by_sign(cls, sign):
        """
        根据标签加载对象
        :param sign: 标签
        :return: 加载对象
        """
        _instance = cls()
        _instance.sign = sign
        return _instance

    @classmethod
    def loads(cls, value):
        """
        根据任意数据进行加载
        :param value: 任意数据
        :return: 加载对象
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
        权限合并
        :param other: 另一个权限
        :return: 权限合并结果
        """
        return self | other

    def __radd__(self, other):
        """
        权限合并
        :param other: 另一个权限
        :return: 权限合并结果
        """
        return self + other

    def __or__(self, other):
        """
        权限合并
        :param other: 另一个权限
        :return: 权限合并结果
        """
        _other = self.loads(other)
        return self.__class__(
            readable=self.readable or _other.readable,
            writable=self.writable or _other.writable,
            executable=self.executable or _other.executable,
        )

    def __ror__(self, other):
        """
        权限合并
        :param other: 另一个权限
        :return: 权限合并结果
        """
        return self | other

    def __sub__(self, other):
        """
        权限去除
        :param other: 另一个权限
        :return: 权限去除结果
        """
        _other = self.loads(other)
        return self.__class__(
            readable=self.readable and not _other.readable,
            writable=self.writable and not _other.writable,
            executable=self.executable and not _other.executable,
        )

    def __rsub__(self, other):
        """
        权限去除
        :param other: 另一个权限
        :return: 权限去除结果
        """
        return self.loads(other) - self

    def __and__(self, other):
        """
        权限且
        :param other: 另一个权限
        :return: 权限且结果
        """
        _other = self.loads(other)
        return self.__class__(
            readable=self.readable and _other.readable,
            writable=self.writable and _other.writable,
            executable=self.executable and _other.executable,
        )

    def __rand__(self, other):
        """
        权限且
        :param other: 另一个权限
        :return: 权限且结果
        """
        return self & other
