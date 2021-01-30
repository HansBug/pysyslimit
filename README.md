# pysystem

`pysystem`是一款基于linux权限系统的简易封装。

## 安装

### 准备工作

在正式安装之前，首先需要进行一些准备：

* 完整的python环境（推荐使用`python 3.5+`）
* unix运行环境
* 【推荐】完整的pip3环境（推荐使用`pip3 18.0`或更高版本）

该包无额外依赖，故不需要进行较多的准备。

### 安装pysystem

接下来安装pysystem包

```bash
git clone -b release https://gitlab.buaaoo.top/oo_course_2019/pysystem.git
cd pysystem
sudo pip3 install .
```

注意：这步操作需要sudo权限。

类似的，卸载pysystem

```bash
sudo pip3 uninstall -y pysystem
```

在安装和卸载的过程中，推荐使用pip进行操作，可以省去很多不必要的麻烦。

## 开始使用

**请注意，该包内的很多操作，都建议在root权限下运行。**

### 查看当前用户与用户组

```python
from pysystem import *

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
from pysystem import *

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