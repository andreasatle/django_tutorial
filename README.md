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

In Django, the path() function is used in URL configurations to map a specific URL pattern to a corresponding view function.

In the code snippet you provided:

,
"" is the URL pattern. In this case, it's an empty string, which means this pattern will match the root URL of your website (e.g., http://www.yourwebsite.com/).

views.index is the view function that will be called when this URL pattern is matched. When a user visits the root URL of your website, Django will call the index function from your views module.

name="index" is an optional parameter that assigns a name to this URL pattern. This name can be used to refer to this specific URL pattern elsewhere in your code, such as in templates. This is particularly useful when you want to create a hyperlink to this URL.