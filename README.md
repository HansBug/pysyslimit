# pysyslimit

[![PyPI](https://img.shields.io/pypi/v/pysyslimit)](https://pypi.org/project/pysyslimit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysyslimit)](https://pypi.org/project/pysyslimit/)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/cab917f712d04db56dbc5dec8b275667/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/cab917f712d04db56dbc5dec8b275667/raw/comments.json)

[![Docs Deploy](https://github.com/HansBug/pysyslimit/workflows/Docs%20Deploy/badge.svg)](https://github.com/HansBug/pysyslimit/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/HansBug/pysyslimit/workflows/Code%20Test/badge.svg)](https://github.com/HansBug/pysyslimit/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/HansBug/pysyslimit/workflows/Badge%20Creation/badge.svg)](https://github.com/HansBug/pysyslimit/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/HansBug/pysyslimit/workflows/Package%20Release/badge.svg)](https://github.com/HansBug/pysyslimit/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/HansBug/pysyslimit/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/HansBug/pysyslimit)

[![GitHub stars](https://img.shields.io/github/stars/HansBug/pysyslimit)](https://github.com/HansBug/pysyslimit/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/HansBug/pysyslimit)](https://github.com/HansBug/pysyslimit/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/HansBug/pysyslimit)
[![GitHub issues](https://img.shields.io/github/issues/HansBug/pysyslimit)](https://github.com/HansBug/pysyslimit/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/HansBug/pysyslimit)](https://github.com/HansBug/pysyslimit/pulls)
[![Contributors](https://img.shields.io/github/contributors/HansBug/pysyslimit)](https://github.com/HansBug/pysyslimit/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/HansBug/pysyslimit)](https://github.com/HansBug/pysyslimit/blob/master/LICENSE)


`pysyslimit`是一款基于linux权限系统的简易封装。

## 安装

### 准备工作

在正式安装之前，首先需要进行一些准备：

* 完整的python环境（推荐使用`python 3.5+`）
* unix运行环境
* 【推荐】完整的pip3环境（推荐使用`pip3 18.0`或更高版本）

该包无额外依赖，故不需要进行较多的准备。

### 安装pysyslimit

接下来安装pysyslimit包

```bash
git clone -b release https://gitlab.buaaoo.top/oo_course_2019/pysyslimit.git
cd pysyslimit
sudo pip3 install .
```

注意：这步操作需要sudo权限。

类似的，卸载pysyslimit

```bash
sudo pip3 uninstall -y pysyslimit
```

在安装和卸载的过程中，推荐使用pip进行操作，可以省去很多不必要的麻烦。

## 开始使用

**请注意，该包内的很多操作，都建议在root权限下运行。**

### 查看当前用户与用户组

```python
from pysyslimit import *

if __name__ == "__main__":
    print("current user", SystemUser.current())
    print("current user's group", SystemUser.current().groups)
    print("current group", SystemGroup.current())

```

输出

```text
current user <SystemUser vagrant, id: 1000>
current user's group <SystemGroup vagrant, id: 1000>
current group <SystemGroup vagrant, id: 1000>
```

### 查看并修改文件权限

```python
from pysyslimit import *

if __name__ == "__main__":
    chmod_del("/home/vagrant", "004")
    _auth = FileAuthority.load_from_file("/home/vagrant")
    print(_auth)
    chmod_add("/home/vagrant", "004")
    _auth = FileAuthority.load_from_file("/home/vagrant")
    print(_auth)

```

输出

```text
rwxr-x--x
rwxr-xr-x
```