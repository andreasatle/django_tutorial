# Create a Django Project

In order to start a new django project using poetry (already installed) to manage python packages etc, I wrote those commands:
```bash
# Create a new poetry project
poetry new Django-tutorial

# Enter the project directory
cd Django-tutorial

# Install django and some more packages for DB management
poetry add django python-dotenv mysqlclient

# Start a shell with the correct environment
poetry shell

# Remove the django_tutorial directory created by poetry
rm -rf django_tutorial

# Start a new django project
django-admin startproject django_tutorial

# Enter the django project
cd django_tutorial

# Start the default web-server
python -m manage runserver
```

In order to use `poetry` properly, I might have to add an `__init__.py` file to the `django_tutorial` directory after it was created with `django-admin`.

# Create a Django App (under the Project)
In the project root-directory, we can create a new app:
```bash
python manage.py startapp polls
```