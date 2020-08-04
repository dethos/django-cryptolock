#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from django_cryptolock/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("django_cryptolock", "__init__.py")


if sys.argv[-1] == "publish":
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

with open("requirements.txt", "r") as f:
    requirements = [req.strip() for req in f.readlines()]

setup(
    name="django-cryptolock",
    version=version,
    description="""Django authentication using cryptocurrency wallets""",
    long_description=readme + "\n\n" + history,
    author="Gonçalo Valério",
    author_email="gon@ovalerio.net",
    url="https://github.com/dethos/django-cryptolock",
    packages=["django_cryptolock"],
    include_package_data=True,
    install_requires=requirements,
    extras_require={"drf": ["djangorestframework>=3.9.3"]},
    license="MIT",
    zip_safe=False,
    keywords="django-cryptolock",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
