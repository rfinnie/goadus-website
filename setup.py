#!/usr/bin/env python3

from setuptools import setup


setup(
    name="goadus",
    description="goad.us",
    author="Ryan Finnie",
    packages=["goadus", "goadus.migrations", "goadus.management.commands"],
    include_package_data=True,
    install_requires=[
        "Django",
        "django[argon2]",
        "django-crispy-forms",
        "crispy-bootstrap4",
        "Pillow",
        "pillow-heif",
        "tzdata",
    ],
)
