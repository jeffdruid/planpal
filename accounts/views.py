from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from events.models import Event
from invitations.models import Invitation
from .models import UserProfile, Friendship
from .forms import FriendSearchForm, ProfilePictureForm
from django.db.models import Q
from notifications.models import Notification
from django.urls import reverse


@login_required
def dashboard(request):
    current_user = request.user

    # Get current datetime
    current_datetime = timezone.now()

    # Get all events created by the user
    user_created_events = Event.objects.filter(
        created_by=current_user
    ).order_by("proposed_date")

    # Get all events the user is invited to
    invited_events = Event.objects.filter(
        invitations__user=current_user
    ).order_by("proposed_date")

    # Combine both querysets for the calendar
    all_events = (
        (user_created_events | invited_events)
        .distinct()
        .order_by("proposed_date")
    )

    # Combine both querysets for upcoming events
    upcoming_events = all_events.filter(proposed_date__gte=current_datetime)

    # Prepare the list of upcoming events with their read status and response status
    upcoming_events_with_read_status = []
    for event in upcoming_events:
        invitation = Invitation.objects.filter(
            event=event, user=current_user
        ).first()
        unread = invitation.read == False if invitation else False
        response_status = invitation.status if invitation else None
        upcoming_events_with_read_status.append(
            {
                "event": event,
                "unread": unread,
                "response_status": response_status,
            }
        )

    # Prepare the list of all events for the calendar
    all_events_with_status = []
    for event in all_events:
        invitation = Invitation.objects.filter(
            event=event, user=current_user
        ).first()
        response_status = invitation.status if invitation else None
        all_events_with_status.append(
            {"event": event, "response_status": response_status}
        )

    context = {
        "upcoming_events_with_read_status": upcoming_events_with_read_status,
        "user_events": user_created_events,  # List of events created by the user
        "all_events_with_status": all_events_with_status,  # List of all events for the calendar
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


@login_required
def friends_page(request):
    current_user = request.user

    search_query = ""
    search_results = []
    if "search_query" in request.GET or "user" in request.GET:
        search_form = FriendSearchForm(request.GET)
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get("search_query", "")
            selected_user = search_form.cleaned_data.get("user")
            if selected_user:
                search_results = [selected_user]
            else:
                search_results = User.objects.filter(
                    Q(username__icontains=search_query)
                    | Q(first_name__icontains=search_query)
                    | Q(last_name__icontains=search_query)
                ).exclude(id=current_user.id)
        else:
            search_results = []
    else:
        search_form = FriendSearchForm()
        search_results = []

    # Get friends and pending requests
    friends = Friendship.objects.filter(
        (Q(from_user=current_user) | Q(to_user=current_user))
        & Q(status="accepted")
    )
    pending_requests_received = Friendship.objects.filter(
        Q(to_user=current_user) & Q(status="pending")
    )
    pending_requests_sent = Friendship.objects.filter(
        Q(from_user=current_user) & Q(status="pending")
    )

    context = {
        "search_form": search_form,
        "search_query": search_query,
        "search_results": search_results,
        "friends": friends,
        "pending_requests_received": pending_requests_received,
        "pending_requests_sent": pending_requests_sent,
    }
    return render(request, "accounts/friends.html", context)


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    from_user = request.user
    friendship = Friendship.objects.filter(
        Q(from_user=from_user, to_user=to_user)
        | Q(from_user=to_user, to_user=from_user)
    ).first()

    if friendship:
        if friendship.status == "accepted":
            messages.error(request, "You are already friends.")
        elif friendship.status == "pending":
            messages.error(request, "Friend request already sent.")
        elif (
            friendship.status == "declined" and friendship.to_user == from_user
        ):
            friendship.status = "pending"
            friendship.from_user = from_user
            friendship.to_user = to_user
            friendship.save()
            Notification.objects.create(
                user=to_user,
                event=None,
                type="friend_request_received",
                message=f"{from_user.username} has sent you a friend request.",
                url=reverse("friends_page"),
            )
            messages.success(request, "Friend request sent successfully.")
        else:
            messages.error(request, "Unable to send friend request.")
    else:
        Friendship.objects.create(
            from_user=from_user, to_user=to_user, status="pending"
        )
        Notification.objects.create(
            user=to_user,
            event=None,
            type="friend_request_received",
            message=f"{from_user.username} has sent you a friend request.",
            url=reverse("friends_page"),
        )
        messages.success(request, "Friend request sent successfully.")

    # Redirect with the current search query
    search_query = request.GET.get("search_query", "")
    return redirect(f"{reverse('friends_page')}?search_query={search_query}")


@login_required
def respond_friend_request(request, request_id, response):
    friend_request = get_object_or_404(Friendship, id=request_id)
    if response == "accept":
        friend_request.status = "accepted"
        messages.success(request, "Friend request accepted.")
    elif response == "decline":
        friend_request.status = "declined"
        messages.success(request, "Friend request declined.")
    friend_request.save()
    return redirect("friends_page")


@login_required
def delete_friend(request, user_id):
    current_user = request.user
    friend = get_object_or_404(User, id=user_id)
    friendships = Friendship.objects.filter(
        Q(from_user=current_user, to_user=friend)
        | Q(from_user=friend, to_user=current_user)
    )
    if friendships.exists():
        friendships.delete()
        messages.success(request, "Friend deleted successfully.")
    else:
        messages.error(request, "Friendship does not exist.")

    return redirect("friends_page")


@login_required
def view_profile(request, user_id):
    friend_profile = get_object_or_404(UserProfile, user__id=user_id)
    friend_user = friend_profile.user  # Retrieve User object from UserProfile
    context = {
        "user_data": {
            "username": friend_user.username,
            "first_name": friend_user.first_name,
            "last_name": friend_user.last_name,
            "profile_picture": friend_profile.profile_picture,
        },
        "view_only": True,
    }
    return render(request, "accounts/profile.html", context)
