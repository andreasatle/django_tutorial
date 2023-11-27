"""
URL patterns for the polls app.

This module defines the URL patterns for the polls app in the Django project.
The urlpatterns list contains a single path that maps the root URL to the index view.

Example:
    urlpatterns = [
        path("", views.index, name="index"),
    ]
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
