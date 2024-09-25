#!/bin/bash
set -e

# git pull {repo_url_here}

# `pyenv activate {the_working_virtualenv_or_python_version_here}`
## example: `pyenv activate medusa`

# install all requirements
pip install -r requirements.txt

# move to main application dir
cd bgsos

# collection static assets
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Start the Gunicorn server, it will serve at port :80
gunicorn -c python:bgsos.gunicorn bgsos.asgi:application
