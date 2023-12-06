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

In order to get reasonable representation of the data, we can modify `polls/admin.py`:
```python
from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
```

I don't know the details of how to make things work in a controlled manner. I can't get the creation and update times to show up. They were implemented in an abstract class. It will take some playing around to fully understand the admin stuff.

# Template namespacing
Now we might be able to get away with putting our templates directly in polls/templates (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first template it finds whose name matches, and if you had a template with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the best way to ensure this is by namespacing them. That is, by putting those templates inside another directory named for the application itself.

# Use a template
In `polls/template/polls/index.html` write a template:
```python
{% if questions %}
<ul>
    {% for question in questions %}
    <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
</ul>
{% else %}
<p>No polls are available.</p>
{% endif %}
```

# Shortcuts with 404
In order to detect 404-errors, we can use
```python
from django.shortcuts import get_object_or_404
def detail(request, question_id):
    return render(request, 'polls/detail.html', {
        "question": get_object_or_404(Question, pk=question_id),
    })
```

The `get_object_or_404` will raise an `Http404` exception if the object is not retrieved. This will show a default 404-page.

# Custom 404-page
After messing around with custom made 404-pages for about half a day without success, I finally found a trivial solution.
All modifications are in the `settings.py`.
```python
...
# Remove debug-mode
DEBUG = False
# Set allowed hosts, a must when not debug.
ALLOWED_HOSTS = ['*']
# Set the default template directory, where we will put a `404.html`.
import os
BASE_DIR = Path(__file__).resolve().parent.parent # Already there...
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        ...
    }
]
```

Finally we just need to provide `templates/404.html`:
```python
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 ERROR</title>
</head>

<body>
    <h1>404 ERROR</h1>
    {% if request_path %}
    <h2>Page '{{request_path}}' not found!</h2>
    {% endif %}
    {% if exception %}
    <h3>{{exception}}</h3>
    {% endif %}
</body>

</html>
```

# Remove hardcoded URLs in templates
In the `polls/templates/polls/index.html` we have a hardcoded url:
```python
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```

We can use a *template tag* to softcode it instead:
```python
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

In the `polls.url` module, we have named the detail view:
```python
path("<int:question_id>/", views.detail, name="detail"),
```

Now if you want to change the URL for the `detail` view, there is only one place to change:
```python
path("new_url/<int:question_id>/", views.detail, name="detail"),
```

Since the template is using the name of the path, rather than the URL directly, it stays unchanged.

# Namespacing URL names
When we have different apps in a project that has the same path-names, we need a way to distinguish those. This is done by namespacing, by setting `polls.url.app_name = 'polls'`

The template has to change to using the introduced namespace:
```python
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

# Generic views

Django provides a set of generic class-based views that simplify the development of common patterns in web applications. These views are designed to handle common tasks and reduce the amount of boilerplate code developers need to write. Here are some of the main generic views in Django:

1. **DetailView:**
   - Used for displaying details of a single object. It's often used to show information about a specific database record. Requires specifying the model and template.

   ```python
   from django.views.generic import DetailView
   from .models import MyModel

   class MyModelDetailView(DetailView):
       model = MyModel
       template_name = 'myapp/mymodel_detail.html'
   ```

2. **ListView:**
   - Used for displaying a list of objects. It's commonly used for displaying a list of records from a database. Requires specifying the model and template.

   ```python
   from django.views.generic import ListView
   from .models import MyModel

   class MyModelListView(ListView):
       model = MyModel
       template_name = 'myapp/mymodel_list.html'
   ```

3. **CreateView:**
   - Used for handling the creation of a new object. It includes a form for user input and takes care of saving the new object to the database.

   ```python
   from django.views.generic import CreateView
   from .models import MyModel

   class MyModelCreateView(CreateView):
       model = MyModel
       template_name = 'myapp/mymodel_form.html'
       fields = ['field1', 'field2']
   ```

4. **UpdateView:**
   - Similar to `CreateView`, but used for updating an existing object. It includes a form pre-filled with the current data and updates the object in the database upon submission.

   ```python
   from django.views.generic import UpdateView
   from .models import MyModel

   class MyModelUpdateView(UpdateView):
       model = MyModel
       template_name = 'myapp/mymodel_form.html'
       fields = ['field1', 'field2']
   ```

5. **DeleteView:**
   - Used for handling the deletion of an object. It displays a confirmation page before deleting the object from the database.

   ```python
   from django.views.generic import DeleteView
   from django.urls import reverse_lazy
   from .models import MyModel

   class MyModelDeleteView(DeleteView):
       model = MyModel
       template_name = 'myapp/mymodel_confirm_delete.html'
       success_url = reverse_lazy('mymodel-list')
   ```

6. **TemplateView:**
   - A simple view that renders a template without any specific model. It's often used for static or informational pages.

   ```python
   from django.views.generic import TemplateView

   class AboutView(TemplateView):
       template_name = 'about.html'
   ```

These generic views are powerful tools for quickly building common patterns in web applications. They encapsulate a lot of functionality, making it easier to create views with less code. Developers can customize these views by overriding certain methods or attributes to fit their specific needs.

## ListView
In Django, `ListView` is a class-based view that is part of the generic views provided by the Django framework. It is designed to simplify the implementation of views for displaying lists of objects. `ListView` is particularly useful for handling the common pattern of displaying a list of items from a database.

Here is a basic explanation of the `ListView` class in Django:

### Purpose:
The `ListView` class is used to display a list of objects retrieved from a database query. It is commonly associated with a Django model, and it simplifies the process of fetching and rendering a list of instances of that model.

### Key Attributes and Methods:

1. **model:**
   - The `model` attribute specifies the Django model class for which the list view is designed. This helps Django to understand from which database table to retrieve the objects.

2. **template_name:**
   - The `template_name` attribute allows you to specify the template used to render the list view. By default, Django looks for a template named `<app_name>/<model_name>_list.html`.

3. **context_object_name:**
   - The `context_object_name` attribute allows you to set the variable name used in the template to represent the list of objects. By default, it is set to `'object_list'`.

4. **queryset:**
   - The `queryset` attribute allows you to define the query used to fetch the list of objects. By default, it retrieves all objects of the specified model.

5. **paginate_by:**
   - If your list of objects is long, you might want to paginate the results. The `paginate_by` attribute allows you to specify the number of objects to display per page.

6. **get_queryset():**
   - This method is used to customize the queryset. You can override this method to filter or modify the queryset based on your specific requirements.

7. **get_context_data():**
   - This method is used to customize the context data passed to the template. You can override it to add extra context variables.

## DetailView
In Django, the detail view is a view that displays detailed information about a specific instance of a model. It is commonly used in web applications to show the details of a single database record, such as a specific blog post, product, user profile, or any other data stored in the database.

Here are the key components and concepts related to the detail view in Django:

1. **Model:**
   - The detail view typically revolves around a specific model in your Django application. This model represents the type of data you want to display details for. For example, if you have a model for blog posts, the detail view might display information about a single blog post.

2. **URL Configuration:**
   - In your Django project, you need to define a URL pattern that maps to the detail view. This pattern includes a parameter (usually the primary key or another unique identifier) that identifies the specific instance of the model.

   ```python
   # Example URL pattern for a blog post detail view
   path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail')
   ```

3. **DetailView Class:**
   - Django provides a generic class-based view called `DetailView` that simplifies the process of creating detail views. You need to create a subclass of `DetailView` and specify the model and template to use.

   ```python
   from django.views.generic import DetailView
   from .models import Post

   class PostDetailView(DetailView):
       model = Post
       template_name = 'blog/post_detail.html'
       context_object_name = 'post'
   ```

4. **Template:**
   - You'll need to create a template (HTML file) that defines how the detailed information should be presented. The template can access the model instance using the specified `context_object_name`.

   ```html
   <!-- Example blog post detail template -->
   <h1>{{ post.title }}</h1>
   <p>{{ post.content }}</p>
   ```

5. **Context Data:**
   - The `DetailView` automatically provides the template with context data containing the instance of the model. You can customize this by setting the `context_object_name` attribute in your view.

6. **Request Flow:**
   - When a user accesses a URL associated with the detail view, Django retrieves the corresponding model instance based on the provided identifier. The view renders the template, injecting the model instance into the context, and returns the rendered HTML to the user's browser.

By using the detail view, you can create a clean and reusable way to display detailed information about specific database records in your Django web application.