import os
import re
import subprocess


class ExecuteException(Exception):
    """
    程序执行异常
    """

    def __init__(self, return_code, stdout, stderr):
        """
        构造函数
        :param return_code: 返回值
        :param stdout: 标准输出
        :param stderr: 标准异常
        """
        self.__return_code = return_code
        self.__stdout = stdout
        self.__stderr = stderr
        super().__init__(self.title)

    @property
    def return_code(self):
        """
        获取返回值
        :return: 返回值
        """
        return self.__return_code

    @property
    def stdout(self):
        """
        获取标准输出
        :return: 标准输出
        """
        return self.__stdout

    @property
    def stderr(self):
        """
        获取标准异常
        :return: 标准异常
        """
        return self.__stderr

    @property
    def message(self):
        """
        获取异常信息
        :return: 异常信息
        """
        return self.__stderr or self.__stdout

    @property
    def title(self):
        """
        返回异常标题
        :return: 异常标题
        """
        _message = self.message
        if _message:
            return re.split(r"[\r\n]+", str(_message))[0]
        else:
            return None


def execute(args, env=None, encoding=None):
    """
    执行指令
    :param args: 命令行参数
    :param env: 环境变量
    :param encoding: 编码格式
    :return: return_code, stdout, stderr
    """
    _encoding = encoding or "utf8"
    env = env or os.environ
    _process = subprocess.Popen(
        args=[str(_arg) for _arg in args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )

    _stdout_bytes, _stderr_bytes = _process.communicate()
    _stdout = _stdout_bytes.decode(_encoding)
    _stderr = _stderr_bytes.decode(_encoding)

    return _process.returncode, _stdout, _stderr


def execute_process(args, env=None, encoding=None, cls=None):
    """
    执行指令（遇到非零返回值会直接抛出异常）
    :param args: 命令行参数
    :param env: 环境变量
    :param encoding: 编码格式
    :param cls: 异常类格式
    :return: return_code, stdout, stderr
    """
    _cls = cls or ExecuteException
    _return_code, _stdout, _stderr = execute(args=args, env=env, encoding=encoding)
    if _return_code == 0:
        return _return_code, _stdout, _stderr
    else:
        raise _cls(return_code=_return_code, stdout=_stdout, stderr=_stderr)
