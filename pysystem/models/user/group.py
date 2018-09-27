import grp
import os


class SystemGroup(object):
    """
    系统用户组类
    """
    __nogroup_group = "nogroup"
    __root_group = "root"

    def __init__(self, gid=None, name=None):
        """
        构造函数（gid和name同时存在时gid优先）
        :param gid: 用户组id
        :param name: 用户组名
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
        获取用户组名
        :return: 用户组名
        """
        return self.__object.gr_name

    @property
    def passwd(self):
        """
        获取密码（？）
        :return: 密码（？）
        """
        return self.__object.gr_passwd

    @property
    def gid(self):
        """
        获取用户组id
        :return: 用户组id
        """
        return self.__object.gr_gid

    @property
    def mem(self):
        """
        获取用户组mem
        :return: 用户组mem
        """
        return self.__object.gr_mem

    def apply(self):
        """
        将gid设置到当前程序
        :return: None
        """
        os.setgroups([self.gid])

    def __repr__(self):
        """
        获取表达形式
        :return: 表达形式
        """
        return r'<%s %s, id: %s>' % (
            type(self).__name__,
            self.name,
            self.gid
        )

    @classmethod
    def current(cls):
        """
        获取当前用户组
        :return: 当前用户组
        """
        return cls()

    @classmethod
    def root(cls):
        """
        获取root用户组
        :return: root用户组
        """
        return cls(name=cls.__root_group)

    @classmethod
    def nogroup(cls):
        """
        获取nogroup用户组
        :return: nogroup用户组
        """
        return cls(name=cls.__nogroup_group)

    @classmethod
    def load_from_file(cls, filename):
        """
        获取文件所有组
        :param filename: 文件名
        :return: 所有组
        """
        return cls(gid=os.stat(filename).st_gid)

    @classmethod
    def loads(cls, value):
        """
        自动加载用户组对象
        :param value: 加载值
        :return: 用户组对象
        """
        if isinstance(value, int):
            return cls(gid=value)
        elif isinstance(value, cls):
            return value
        else:
            return cls(name=str(value))
