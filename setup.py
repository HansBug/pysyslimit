from distutils.core import setup

from setuptools import find_packages

_package_name = "pysystem"
_version = "0.1"
setup(
    name=_package_name,
    version=_version,
    packages=find_packages(
        include=(_package_name, "%s.*" % _package_name)
    )
)
