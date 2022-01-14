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

`pysyslimit` is a light-weight library which can manage the permission in linux system.

## Installation

Just install this package with the pip command

```bash
pip install pysyslimit
```

For further information, take a look at the [Installation Page](https://hansbug.github.io/pysyslimit/main/tutorials/installation/index.html).

## Quick Start

**Please attention that many function in this library need root permission, so It is strongly recommended to run this with root.**

### Take a look at who I am

```python
from pysyslimit import *

if __name__ == "__main__":
    print("current user:", SystemUser.current())
    print("current user's groups:", SystemUser.current().groups)
    print("current group:", SystemGroup.current())

```

The output should be

```text
current user: root
current user's groups: [<SystemGroup root, id: 0>]
current group: root
```

### Get and update the permission of files

```python
from pysyslimit import *

if __name__ == "__main__":
    print(FilePermission.load_from_file("test_file"))

    chmod_del("test_file", "004")
    print(FilePermission.load_from_file("test_file"))

    chmod_add("test_file", "014")
    print(FilePermission.load_from_file("test_file"))

```

The output shall be

```text
rw-rw-r--
rw-rw----
rw-rwxr--
```

### Do calculation between permissions

```python
from pysyslimit import *

if __name__ == "__main__":
    print(FilePermission.loads('463') + FilePermission.loads('615'))
    print(FilePermission.loads('463') | FilePermission.loads('615'))  # the same as +
    print(FilePermission.loads('463') - FilePermission.loads('615'))
    print(FilePermission.loads('463') & FilePermission.loads('615'))

```

The output shall be

```text
rw-rwxrwx
rw-rwxrwx
---rw--w-
r-------x
```



# Contributing

We appreciate all contributions to improve `pysyslimit` ,both logic and system designs. Please refer to CONTRIBUTING.md for more guides.

# License

`pysyslimit` released under the Apache 2.0 license.