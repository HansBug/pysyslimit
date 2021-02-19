import os
import re

from .single import FileSingleAuthority, _BaseVariables


class FileUserAuthority(FileSingleAuthority):
    """
    用户权限类
    """
    pass


class FileGroupAuthority(FileSingleAuthority):
    """
    用户组权限类
    """
    pass


class FileOtherAuthority(FileSingleAuthority):
    """
    其他权限类
    """
    pass


class FileAuthority(_BaseVariables):
    """
    文件权限类
    """

    def __init__(self, user_authority=None, group_authority=None, other_authority=None):
        """
        构造函数
        :param user_authority: 用户权限对象
        :param group_authority: 用户组权限对象
        :param other_authority: 其他权限对象
        """
        self.__user_authority = FileUserAuthority.loads(user_authority or FileUserAuthority())
        self.__group_authority = FileGroupAuthority.loads(group_authority or FileGroupAuthority())
        self.__other_authority = FileOtherAuthority.loads(other_authority or FileOtherAuthority())

    @property
    def user(self):
        """
        获取用户权限
        :return: 用户权限
        """
        return self.__user_authority

    @user.setter
    def user(self, value):
        """
        设置用户权限
        :param value: 用户权限
        """
        self.__user_authority = FileUserAuthority.loads(value)

    @property
    def group(self):
        """
        获取用户组权限
        :return: 用户组权限
        """
        return self.__group_authority

    @group.setter
    def group(self, value):
        """
        设置用户组权限
        :param value: 用户组权限
        """
        self.__group_authority = FileGroupAuthority.loads(value)

    @property
    def other(self):
        """
        获取其他权限
        :return: 其他权限
        """
        return self.__other_authority

    @other.setter
    def other(self, value):
        """
        设置其他权限
        :param value: 其他权限
        """
        self.__other_authority = FileOtherAuthority.loads(value)

    @property
    def sign(self):
        """
        获取权限标记串
        :return: 权限标记串
        """
        return "%s%s%s" % (
            self.__user_authority.sign,
            self.__group_authority.sign,
            self.__other_authority.sign,
        )

    @sign.setter
    def sign(self, value):
        """
        设置权限标记串
        :param value: 权限标记串
        """
        if isinstance(value, str):
            if re.fullmatch(self._FULL_SIGN, value):
                self.__user_authority.sign = value[0:3]
                self.__group_authority.sign = value[3:6]
                self.__other_authority.sign = value[6:9]
            else:
                raise ValueError('Invalid single sign - {actual}.'.format(actual=repr(value)))
        else:
            raise TypeError('Str expected but {actual} found.'.format(actual=repr(type(value))))

    def __str__(self):
        """
        获取字符串格式（即权限标记串）
        :return: 字符串格式
        """
        return self.sign

    @property
    def value(self):
        """
        获取权限值（十进制）
        :return: 权限值（十进制）
        """
        return sum([
            self.__user_authority.value * 64,
            self.__group_authority.value * 8,
            self.__other_authority.value * 1,
        ])

    @value.setter
    def value(self, val):
        """
        设置权限值（十进制）
        :param val: 权限值（十进制）
        """
        if isinstance(val, str):
            if not re.fullmatch(self._FULL_DIGIT, val):
                raise ValueError('3-length digit expected but {actual} found.'.format(actual=repr(val)))
            val = int(val, 8)

        if isinstance(val, int):
            if val >= self._FULL_WEIGHT:
                raise ValueError('Value from 000 to 777 expected but {actual} found.'.format(actual=repr(oct(val)[2:])))
        else:
            raise TypeError('Integer or integer-like string expected but {actual} found.'.format(actual=repr(val)))

        self.__user_authority.value = int(val / 64) & 7
        self.__group_authority.value = int(val / 8) & 7
        self.__other_authority.value = int(val / 1) & 7

    def __int__(self):
        """
        获取整型类型
        :return: 整型类型
        """
        return self.value

    @property
    def oct_value(self):
        """
        获取八进制数值
        :return: 八进制数值
        """
        _value = oct(self.value)[2:]
        _value = "0" * (3 - len(_value)) + _value
        return _value

    @oct_value.setter
    def oct_value(self, value):
        """
        设置八进制数值
        :param value: 八进制数值
        """
        # noinspection PyAttributeOutsideInit
        self.value = int(str(value), 8)

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
        :param value: 数值
        :return: 加载对象
        """
        _instance = cls()
        _instance.value = value
        return _instance

    @classmethod
    def load_by_sign(cls, sign):
        """
        根据权限标记串加载对象
        :param sign: 权限标记串
        :return: 加载对象
        """
        _instance = cls()
        _instance.sign = sign
        return _instance

    @classmethod
    def load_by_oct_value(cls, oct_value):
        """
        根据八进制值加载对象
        :param oct_value: 八进制值
        :return: 加载对象
        """
        _instance = cls()
        _instance.oct_value = oct_value
        return _instance

    @classmethod
    def loads(cls, value):
        """
        根据各类值加载对象
        :param value: 各类值
        :return: 加载对象
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
        根据文件加载对象
        :param filename: 文件名
        :return: 加载对象
        """
        return cls.load_by_value(os.stat(filename).st_mode & cls._FULL_MASK)

    def __or__(self, other):
        """
        权限合并
        :param other: 另一个权限
        :return: 权限合并结果
        """
        _other = self.loads(other)
        return self.__class__(
            user_authority=self.__user_authority | _other.__user_authority,
            group_authority=self.__group_authority | _other.__group_authority,
            other_authority=self.__other_authority | _other.__other_authority,
        )

    def __ror__(self, other):
        """
        权限合并
        :param other: 另一个权限
        :return: 权限合并结果
        """
        return self | other

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

    def __and__(self, other):
        """
        权限且
        :param other: 另一个权限
        :return: 权限且结果
        """
        _other = self.loads(other)
        return self.__class__(
            user_authority=self.__user_authority & _other.__user_authority,
            group_authority=self.__group_authority & _other.__group_authority,
            other_authority=self.__other_authority & _other.__other_authority,
        )

    def __rand__(self, other):
        """
        权限且
        :param other: 另一个权限
        :return: 权限且结果
        """
        return self & other

    def __sub__(self, other):
        """
        权限去除
        :param other: 另一个权限
        :return: 权限去除结果
        """
        _other = self.loads(other)
        return self.__class__(
            user_authority=self.__user_authority - _other.__user_authority,
            group_authority=self.__group_authority - _other.__group_authority,
            other_authority=self.__other_authority - _other.__other_authority,
        )

    def __rsub__(self, other):
        """
        权限去除
        :param other: 另一个权限
        :return: 权限去除结果
        """
        return self.loads(other) - self
