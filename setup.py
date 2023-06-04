#!/usr/bin/env python3

from setuptools import setup


setup(
    name="goadus",
    description="goad.us",
    author="Ryan Finnie",
    packages=["goadus", "goadus.migrations", "goadus.management.commands"],
    include_package_data=True,
    install_requires=["Django<3.2.11", "django-crispy-forms<1.15.0", "Pillow", "tzdata"],
)
