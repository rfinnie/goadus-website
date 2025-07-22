# SPDX-PackageSummary: goadus-website
# SPDX-FileCopyrightText: Copyright (C) 2020-2025 Ryan Finnie
# SPDX-License-Identifier: MPL-2.0
FROM python:3.12

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir gunicorn .

USER nobody
ENV DJANGO_SETTINGS_MODULE="goadus.settings"
ENV PYTHONPATH=/usr/local/lib/python
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "-k", "gthread", "--error-logfile", "-", "--capture-output", "goadus.wsgi:application" ]
EXPOSE 8000/tcp
