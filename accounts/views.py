from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import authenticate, login


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("account_signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("account_signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")
            return redirect("account_signup")

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )
        user.save()

        # Create the user profile
        UserProfile.objects.create(user=user)

        messages.success(request, "Registration successful. Please log in.")
        return redirect("account_login")

    return render(request, "accounts/signup.html")


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
        messages.success(request, "Profile updated successfully.")
        return redirect("dashboard")

    user_data = {
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    }
    return render(request, "accounts/profile.html", {"user_data": user_data})


def custom_login(request):
    if request.method == "POST":
        username = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")
