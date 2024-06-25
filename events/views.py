from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def add_event(request):
    return render(request, "events/add_event.html")
