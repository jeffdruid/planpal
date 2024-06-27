from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "accounts/home.html")


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@login_required
def profile(request):
    # Static user data for now
    user_data = {
        "username": request.user.username,
        "email": request.user.email,
        "first_name": "John",
        "last_name": "Doe",
        "bio": "This is a sample bio.",
    }
    return render(request, "accounts/profile.html", {"user_data": user_data})
