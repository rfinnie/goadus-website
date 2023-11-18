# goad.us website

This is a quick<sup>0</sup> and dirty django port of goad.us, formerly written in PHP.

<sup>0</sup> Not actually quick. It took about 2 full days to replace the functionality of a 300-line hack of a PHP script.

## Local dev
### local_setting.py
```python
import os
from goadus.settings import *

SECRET_KEY = 'LOCAL-DEV-ONLY-98Br2ZMWt99DqxxcNlcSmfdXsdsb8mRpbcP9VXRC'
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')
MEDIA_URL = 'http://127.0.0.1/'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
```
### Set up
```shell
VENV_DIR=~/venv/goadus
export DJANGO_SETTINGS_MODULE=local_settings
python3 -mvirtualenv ~/venv/goadus
${VENV_DIR?}/bin/pip install -r requirements.txt
${VENV_DIR?}/bin/python manage.py migrate
${VENV_DIR?}/bin/python manage.py createsuperuser
${VENV_DIR?}/bin/python manage.py runserver
```
