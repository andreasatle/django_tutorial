from django.http import HttpResponse
from django.shortcuts import render

from .models import Question, Choice

def index(request):
    """
    View function for the index page.

    This view function displays the three most recently published questions.
    """
    return render(request, 'polls/index.html', {
        "questions": Question.objects.order_by("-created_at")[:3],
    })


def detail(request, question_id):
    """
    View function for displaying the details of a specific question.
    """
    return render(request, 'polls/detail.html', {
        "question": Question.objects.get(pk=question_id),
    })
    return HttpResponse(f"You're looking at question {question_id}.")


def results(request, question_id):
    """
    View function for displaying the results of a specific question.
    """
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(request, question_id):
    """
    Casts a vote for a specific question.
    """
    return HttpResponse(f"You're voting on question {question_id}.")