from django.http import HttpResponse

from .models import Question, Choice

def index(request):
    """
    View function for the index page.

    This function retrieves the latest three questions from the database
    and returns a comma-separated string of their question texts.
    """
    response = ", ".join([q.question_text for q in Question.objects.order_by("-created_at")[:3]])
    return HttpResponse(response)


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