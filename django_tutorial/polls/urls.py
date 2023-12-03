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
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
