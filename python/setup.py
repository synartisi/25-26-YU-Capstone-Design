# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="capstone",
    version="0.1.0",
    description="Raspberry Pi controller for multi-joint robotic arm and rover",
    license="MIT",
    author="synartisi",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.13",
    ]
)
