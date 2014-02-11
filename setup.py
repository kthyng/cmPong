#!/usr/bin/env python

"""
setup.py for cmPong

"""
import shutil
from setuptools import setup # to support "develop" mode
from numpy.distutils.core import setup, Extension

setup(
    name = "cmPong",
    version = "0.01",
    author = "Kristen Thyng",
    author_email = "",
    description = ("Colormaps for PONG"),
    long_description=open('README.md').read(),
    classifiers=[
                 "Development Status :: 3 - Alpha",
    #             "Topic :: Utilities",
                 ],
    packages = ["cmPong"],
    # py_modules = modules,
    ext_package='cmPong', 
    scripts = [],
    )
