from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "accounts/home.html")


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@login_required
def profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        return redirect("dashboard")

    user_data = {
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    }
    return render(request, "accounts/profile.html", {"user_data": user_data})
