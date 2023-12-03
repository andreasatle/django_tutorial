from django.http import HttpResponse

def index(request):
    """
    This view function returns a HttpResponse with a greeting message.
    """
    return HttpResponse("Hello, world. You're at the polls index.")


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