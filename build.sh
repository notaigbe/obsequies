#!/usr/bin/env bash

set -o errexit

pipenv install

python manage.py collectstatic --no-input
#python manage.py makemigrations
#python manage.py migrate
