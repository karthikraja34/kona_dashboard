# Kona Dashboard

An emotional welfare dashboard for companies

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Setting up the project
### Create virtualenv with python3
- `python3.9 -m venv <virtual env path>`
- `source <virtual env path>/bin/activate`

### Install Requirements
- `cd <project_root_directory>`
- `pip install -r requirements/base.txt`

### Database setup
- Install Postgres
- `createdb --username=<username> <project_name>`

### Database table creations\
- Set database in Environment
  - export DATABASE_URL=postgres://<username>:<password>@127.0.0.1:5432/<DB name given to createdb>
- `cd <project_root_directory>`
- `./manage.py migrate`

### Running Backend
- Once the above steps are done, then server can be started anytime by running
- `./manage.py runserver`

### Frontend
- `cd frontend`
- `npm i`
- `npm start`
