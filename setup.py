#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mirror-hash",
    version="0.2.0",
    author="José I. O.",
    author_email="jose@orlicki.com",
    description="An experimental hash function based on Toffoli and Fredkin gates for optical/quantum computers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorlicki/mirror-hash",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security :: Cryptography",
        "Topic :: Scientific/Engineering :: Quantum Computing",
    ],
    python_requires=">=3.6",
) 