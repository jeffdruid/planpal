from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.timezone import now
from events.models import Event
from invitations.models import Invitation
from django.contrib import messages
from .models import UserProfile
from .forms import ProfilePictureForm


@login_required
def dashboard(request):
    current_user = request.user

    # Get current datetime
    current_datetime = now()

    # Get events created by the user
    user_events = Event.objects.filter(
        created_by=current_user, proposed_date__gte=current_datetime
    ).order_by("proposed_date")

    # Get events the user is invited to
    invited_events = Event.objects.filter(
        invitations__user=current_user, proposed_date__gte=current_datetime
    ).order_by("proposed_date")

    # Combine both querysets
    upcoming_events = (
        (user_events | invited_events).distinct().order_by("proposed_date")
    )

    # Prepare the list of upcoming events with their read status
    upcoming_events_with_read_status = []
    for event in upcoming_events:
        unread_invitations = Invitation.objects.filter(
            event=event, user=current_user, read=False
        ).exists()
        upcoming_events_with_read_status.append(
            {"event": event, "unread": unread_invitations}
        )

    context = {
        "upcoming_events_with_read_status": upcoming_events_with_read_status,
        "user_events": user_events,
    }
    return render(request, "accounts/dashboard.html", context)


def signup(request):
    context = {"errors": [], "success": ""}
    if request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]

            if password1 != password2:
                context["errors"].append("Passwords do not match.")
            elif User.objects.filter(username=username).exists():
                context["errors"].append("Username already taken.")
            elif User.objects.filter(email=email).exists():
                context["errors"].append("Email already taken.")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1
                )
                user.save()

                # Check if the profile already exists
                if not UserProfile.objects.filter(user=user).exists():
                    UserProfile.objects.create(user=user)

                # Automatically log the user in
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect("dashboard")

        except MultiValueDictKeyError as e:
            context["errors"].append(f"Missing field: {str(e)}")

    return render(request, "accounts/signup.html", context)


def home(request):
    return render(request, "accounts/home.html")


@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        profile_form = ProfilePictureForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            request.user.first_name = request.POST.get("first_name")
            request.user.last_name = request.POST.get("last_name")
            request.user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        profile_form = ProfilePictureForm(instance=user_profile)

    user_data = {
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "profile_picture": user_profile.profile_picture,
    }

    context = {
        "user_data": user_data,
        "profile_form": profile_form,
    }

    return render(request, "accounts/profile.html", context)


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
