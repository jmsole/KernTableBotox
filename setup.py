# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="KernTableBotox",
    version="0.2",
    description="a little tool to inject old school kern table in font files",
    long_description=readme(),
    classifiers=[
        "Development Status :: 5 - Beta",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.10.4",
        "Topic :: Software Development :: Build Tools",
    ],
    author="Mathieu Reguer",
    author_email="mathieu.reguer@gmail.com",
    license="All rights reserved",
    packages=find_packages("KernTableBotox"),
    package_dir={"": "KernTableBotox"},
    entry_points={
        "console_scripts": [
            "KernTableBotox = KernTableBotox.KernTableBotox:inject_kern_table",
        ],
    },
    install_requires=[
        "fonttools",
        "click",
    ],
    include_package_data=True,
    zip_safe=False,
)
