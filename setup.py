# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gradrana",
    version="0.0.1",
    author="Christian Lück",
    author_email="christian.lueck@fernuni-hagen.de",
    description="Analyzer for dramatic works",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lueck/pygradrana",
    packages=["gradrana"],#setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        "networkx",
        "Matplotlib"
    ],
    entry_points={
        "console_scripts" : ["dranalyze=gradrana.app:__main__",
                             "gradrana=gradrana.app:__main__"]
    },
)
