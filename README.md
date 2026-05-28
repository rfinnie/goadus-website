# goad.us website

[![Git forge repository](https://img.shields.io/badge/git-forge-orange?logo=forgejo)](https://forge.colobox.com/rfinnie/goadus-website)
[![CI pipeline status](https://woodpecker.colobox.com/api/badges/44/status.svg)](https://woodpecker.colobox.com/repos/44)

This is a quick<sup>0</sup> and dirty django port of goad.us, formerly written in PHP.

<sup>0</sup> Not actually quick. It took about 2 full days to replace the functionality of a 300-line hack of a PHP script.

## Local dev
### goadus/local_settings.py
```python
import os
from goadus.settings import *

SECRET_KEY = 'LOCAL-DEV-ONLY-98Br2ZMWt99DqxxcNlcSmfdXsdsb8mRpbcP9VXRC'
MEDIA_URL = '/media/'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
```
### Set up
```shell
VENV_DIR=~/venv/goadus
export DJANGO_SETTINGS_MODULE=goadus.local_settings
python3 -mvirtualenv ${VENV_DIR?}
${VENV_DIR?}/bin/pip install .
${VENV_DIR?}/bin/django-admin migrate
${VENV_DIR?}/bin/django-admin createsuperuser

${VENV_DIR?}/bin/pip install . && ${VENV_DIR?}/bin/django-admin runserver
```

## License

This document is provided under the following license:

    SPDX-PackageName: goadus-website
    SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
    SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/goadus-website
    SPDX-FileCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
    SPDX-License-Identifier: CC-BY-SA-4.0
