# Django project.
Private cooperative. Information on payments and liabilities. Reporting and data archiving.

## Project setup

## Install Python.
## Install, create and activate Virtualenv in project folder.
```
pip install virtualenv
python3 -m venv venv
venv/scripts/activate
```
## or see: [https://docs.python.org/3/library/venv.html]

### Install project requirements.
```
pip install -r requirements.txt
```
### Setup the Database.
In this case used postgres database. You can use other, but change database settings in settings.py file in the project.
After that run migrations:
```
python manage.py migrate
```
And create super user:
```
python manage.py createsuperuser
```
### Start project:
```
python manage.py runserver
```
