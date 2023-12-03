from django.http import HttpResponse
from django.template import loader

from .models import Question, Choice

def index(request):
    """
    View function for the index page.

    This view function displays the three most recently published questions.
    """
    template = loader.get_template("polls/index.html")
    context = {
        "questions": Question.objects.order_by("-created_at")[:3],
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    """
    View function for displaying the details of a specific question.
    """
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