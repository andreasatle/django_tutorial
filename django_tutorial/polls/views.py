from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    """
    A view that displays a list of the three most recently published questions.
    """
    template_name = "polls/index.html"
    context_object_name = "questions"

    def get_queryset(self):
        """
        Return the three most recently published questions.
        """
        return Question.objects.filter(created_at__lte=timezone.now()).order_by("-created_at")[:3]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def index(request):
    """
    View function for the index page.

    This view function displays the three most recently published questions.
    """
    paginate_by = 2
    return render(request, 'polls/index.html', {
        "questions": Question.objects.order_by("-created_at")[:3],
    })


def detail(request, question_id):
    """
    View function for displaying the details of a specific question.
    """
    return render(request, 'polls/detail.html', {
        "question": get_object_or_404(Question, pk=question_id),
    })


def results(request, question_id):
    """
    View function for displaying the results of a specific question.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    """
    Casts a vote for a specific question.
    """

    question = get_object_or_404(Question, pk=question_id)

    try:
        # The exception arguments for the get method are: (KeyError, Choice.DoesNotExist).
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    except: # (KeyError, Choice.DoesNotExist):

        # Redisplay the question voting form, with an error_message.
        return render(request, "polls/detail.html", {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))