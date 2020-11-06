from distutils.core import setup
from codecs import open

from setuptools import find_packages

from pysystem.configs import package_version as _version

from prepare import _package_name

meta = {}
with open(os.path.join(here, _package_name, 'config', 'meta.py'), 'r', 'utf-8') as f:
    exec(f.read(), meta)


setup(
    name=meta['__TITLE__'],
    version=meta['__VERSION__'],
    packages=find_packages(
        include=(_package_name, "%s.*" % _package_name)
    )
    author=meta['__AUTHOR__'],
    author_email=meta['__AUTHOR_EMAIL__'],
    python_requires=">=3.5"
)
