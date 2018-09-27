import os
import pwd

from .group import SystemGroup


class SystemUser(object):
    """
    系统用户类
    """
    __root_user = "root"
    __nobody_user = "nobody"

    def __init__(self, uid=None, name=None):
        """
        构造函数（uid和uname均存在时以uid优先）
        :param uid: 用户id
        :param name: 用户名
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
        获取用户名
        :return: 用户名
        """
        return self.__object.pw_name

    @property
    def passwd(self):
        """
        获取密码（？）
        :return: 密码（？）
        """
        return self.__object.pw_passwd

    @property
    def uid(self):
        """
        获取用户id
        :return: 用户id
        """
        return self.__object.pw_uid

    @property
    def gid(self):
        """
        获取用户组id
        :return: 用户组id
        """
        return self.__object.pw_gid

    @property
    def gecos(self):
        """
        获取gecos
        :return: gecos
        """
        return self.__object.pw_gecos

    @property
    def dir(self):
        """
        获取用户路径
        :return: 用户路径
        """
        return self.__object.pw_dir

    @property
    def shell(self):
        """
        获取shell命令行路径
        :return: shell命令行路径
        """
        return self.__object.pw_shell

    @property
    def group(self):
        """
        获取用户组对象
        :return: 用户组对象
        """
        return SystemGroup(gid=self.gid)

    def apply(self, include_group=True):
        """
        将uid设置到当前程序
        :param include_group: 是否一并设置gid
        :return: None
        """
        if include_group:
            self.group.apply()
        os.setuid(self.uid)

    def __repr__(self):
        """
        获取表达形式
        :return: 表达形式
        """
        return r'<%s %s, id: %s>' % (
            type(self).__name__,
            self.name,
            self.uid
        )

    @classmethod
    def current(cls):
        """
        获取当前用户
        :return: 当前用户
        """
        return cls()

    @classmethod
    def root(cls):
        """
        获取root用户
        :return: root用户
        """
        return cls(name=cls.__root_user)

    @classmethod
    def nobody(cls):
        """
        获取nobody用户
        :return: nobody用户
        """
        return cls(name=cls.__nobody_user)

    @classmethod
    def load_from_file(cls, filename):
        """
        获取文件所有者
        :param filename: 文件名
        :return: 所有者
        """
        return cls(uid=os.stat(filename).st_uid)

    @classmethod
    def loads(cls, value):
        """
        自动加载用户对象
        :param value: 加载值
        :return: 用户对象
        """
        if isinstance(value, int):
            return cls(uid=value)
        elif isinstance(value, cls):
            return value
        else:
            return cls(name=str(value))