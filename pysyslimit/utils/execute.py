import os
import re
import subprocess


class ExecuteException(Exception):
    """
    Overview:
        Error when the command line execute failed.
    """

    def __init__(self, return_code, stdout, stderr):
        """
        Overview:
            Constructor of class :class:`pysyslimit.utils.ExecuteException`.

        Arguments:
            - return_code: Return code.
            - stdout: Stdout content.
            - stderr: Stderr content.
        """
        assert return_code != 0
        self.__return_code = return_code
        self.__stdout = stdout
        self.__stderr = stderr
        super().__init__(self.title)

    @property
    def return_code(self):
        """
        Overview:
            Return code of this command.
        """
        return self.__return_code

    @property
    def stdout(self):
        """
        Overview:
            Stdout content of this command.
        """
        return self.__stdout

    @property
    def stderr(self):
        """
        Overview:
            Stderr content of this command.
        """
        return self.__stderr

    @property
    def message(self):
        """
        Overview:
            Message of this command.
        """
        return self.__stderr or self.__stdout

    @property
    def title(self):
        """
        Overview:
            Title of this command.
        """
        _message = self.message
        if _message:
            return re.split(r"[\r\n]+", str(_message))[0]
        else:
            return None


def cmd_execute(args, env=None, encoding=None):
    """
    Overview:
        Execute one command line.

    Arguments:
        - args: Command line arguments.
        - env: Environment variables.
        - encoding: Encoding format.

    Returns:
        - tuple: A tuple which is like ``(return_code, stdout, stderr)``.

    Examples::
        >>> from pysyslimit.utils import cmd_execute
        >>> cmd_execute(['echo', '233'])
        (0, '233\\n', '')
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
    Overview:
        Execute process, raise exception when return code is not 0.

    Arguments:
        - args: Command line arguments.
        - env: Environment variables.
        - encoding: Encoding format.
        - cls: Class of exception.

    Returns:
        - tuple: A tuple which is like ``(return_code, stdout, stderr)``.

    Examples::
        >>> from pysyslimit.utils import execute_process
        >>> execute_process(['echo', '233'])
        (0, '233\\n', '')
    """
    _cls = cls or ExecuteException
    _return_code, _stdout, _stderr = cmd_execute(args=args, env=env, encoding=encoding)
    if _return_code == 0:
        return _return_code, _stdout, _stderr
    else:
        raise _cls(return_code=_return_code, stdout=_stdout, stderr=_stderr)
