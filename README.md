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

# Create a first url and view in the polls app
Create a file `polls/urls.py`
```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

and modify `polls/views.py` to
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

# Setup a mySQL database
I first made the mistake of starting with an existing database, while changing the model slightly. Start with an empty database! That makes things easier to get running!

To setup the mySQL database, create a `.env` file in the project root, containing:
```bash
# This should be placed in .env
# replace <...> with user specific values
DB_ENGINE='django.db.backends.mysql'
DB_NAME=<database_name>
DB_USER=<user_name>
DB_PASSWORD=<user_password>
DB_HOST='localhost'
DB_PORT='3306'
```

Remember that we have already installed the python package `mysqlclient`.
If you want to run a different SQL, you have to install a different python package. We have already installed the `python-dotenv` package to not have to hardcode the database definition.

In the `settings.py` file, replace the `DATABASE` section with:
```python
from dotenv import load_dotenv
import os
load_dotenv()
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

# Create the model for the app
In order to communicate with the database, we create a model in the app that corresponds to the tables in the database. For convenience, I deviate slightly from the online tutorial, and create two entries `created_at` and `updated_at`, which appears in an abstract class.

The model is defined in classes, in `polls/models.py`
```python
from django.db import models

class WithTimestamp(models.Model):
    created_at = models.DateTimeField("date published", auto_now_add=True)
    updated_at = models.DateTimeField("date of last change", auto_now=True)

    class Meta:
        abstract = True

class Question(WithTimestamp):
    question_text = models.CharField(max_length=200)

class Choice(WithTimestamp):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

# Add the App in the settings
In order for the project to recognize an app we need to add it to the settings, in `django_tutorial/settings.py`:
```python
INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    ...
]
```

# Migrate models
In order to synchronize the models with the database, we have some management commands:
```bash
python -m manage makemigrations polls
python -m manage migrate
```

# Interact with the database
Start a shell with
```bash
python -m manage shell
```

and write the following:
```python
# Import some packages
>>> from polls.models import Choice, Question

# Check that database is empty
>>> Question.objects.all()
<QuerySet []>
>>> Choice.objects.all()
<QuerySet []>

# Create a question
>>> q = Question(question_text="What's new?")

# Save question to database
>>> q.save()

# Check the timestamp
>>> q.updated_at
datetime.datetime(2023, 12, 3, 1, 51, 35, 394257, tzinfo=datetime.timezone.utc)

# Change the question
>>> q.question_text = 'I have a question for you. What is the question?'

# Save the changes
>>> q.save()

# Check the creation timestamp
>>> q.created_at
datetime.datetime(2023, 12, 3, 1, 51, 35, 393997, tzinfo=datetime.timezone.utc)

# Check that the updated timestamp is later
>>> q.updated_at
datetime.datetime(2023, 12, 3, 1, 52, 45, 654442, tzinfo=datetime.timezone.utc)

# Next add some choices
# First fetch the question
>>> q = Question.objects.get(pk=1)

# Add three choices, no sense here...
>>> q.choice_set.create(choice_text="Not much")
<Choice: Choice object (1)>
>>> q.choice_set.create(choice_text="The sky")
<Choice: Choice object (2)>
>>> q.choice_set.create(choice_text="Just hacking")
<Choice: Choice object (3)>

# Save changes and quit shell
>>> q.save()
>>> quit()
```

# Verify changes with SQL
To access a SQL client in django, you can write
```bash
python -m manage dbshell
```
This will start a mysql client
```bash
mysql> select * from polls_question;
+----+----------------------------+----------------------------+--------------------------------------------------+
| id | created_at                 | updated_at                 | question_text                                    |
+----+----------------------------+----------------------------+--------------------------------------------------+
|  1 | 2023-12-03 01:51:35.393997 | 2023-12-03 01:57:10.901465 | I have a question for you. What is the question? |
+----+----------------------------+----------------------------+--------------------------------------------------+
1 row in set (0.00 sec)

mysql> select * from polls_choice;
+----+----------------------------+----------------------------+--------------+-------+-------------+
| id | created_at                 | updated_at                 | choice_text  | votes | question_id |
+----+----------------------------+----------------------------+--------------+-------+-------------+
|  1 | 2023-12-03 01:55:40.300693 | 2023-12-03 01:55:40.300721 | Not much     |     0 |           1 |
|  2 | 2023-12-03 01:55:48.670681 | 2023-12-03 01:55:48.670705 | The sky      |     0 |           1 |
|  3 | 2023-12-03 01:55:56.290918 | 2023-12-03 01:55:56.290942 | Just hacking |     0 |           1 |
+----+----------------------------+----------------------------+--------------+-------+-------------+
3 rows in set (0.00 sec)
```

This shows that the commands in the python shell actually changed the database.

# Introduce the Django Admin
We can create a new superuser with the command:
```bash
python -m manage createsuperuser
```