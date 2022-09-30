# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="pioreactor_relay_plugin",
    version="0.0.8",
    license="MIT",
    description="Turn your additional hardware (light source, pump) on or off.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author_email="kelly@pioreactor.com",
    author="Kelly Tran",
    url="https://github.com/kellytr/pioreactor-relay-plugin",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "pioreactor.plugins": "pioreactor_relay_plugin = pioreactor_relay_plugin"
    },
)