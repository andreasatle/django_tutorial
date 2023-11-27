from django.http import HttpResponse

def index(request):
    """
    This view function returns a HttpResponse with a greeting message.
    """
    return HttpResponse("Hello, world. You're at the polls index.")