from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from events.models import Event
from invitations.models import Invitation
from .models import UserProfile, Friendship
from .forms import FriendSearchForm, ProfilePictureForm, SignupForm
from django.db.models import Q
from notifications.models import Notification
from django.urls import reverse
from django.views.decorators.cache import cache_control


def custom_400_view(request, exception):
    return render(request, "400.html", status=400)


def custom_403_view(request, exception):
    return render(request, "403.html", status=403)


def custom_404_view(request, exception):
    return render(request, "404.html", status=404)


def custom_500_view(request):
    return render(request, "500.html", status=500)


@login_required
def set_new_password(request):
    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            return redirect("account_login")

    return render(request, "accounts/set_new_password.html")


def password_reset_done(request):
    return render(request, "accounts/password_reset_done.html")


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    current_user = request.user

    # Get current datetime
    current_datetime = timezone.now()

    # Get filter parameter from request
    filter_status = request.GET.get("filter", "all")

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

    # Apply the filter to upcoming events
    if filter_status in ["Accept", "Deny", "Maybe", "Pending"]:
        upcoming_events = upcoming_events.filter(
            invitations__status=filter_status, invitations__user=current_user
        )

    # Prepare the list of upcoming events with their read status
    # and response status
    upcoming_events_with_read_status = []
    for event in upcoming_events:
        invitation = Invitation.objects.filter(
            event=event, user=current_user
        ).first()
        unread = False if invitation and not invitation.read else False
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
        # List of events created by the user
        "user_events": user_created_events,
        "all_events_with_status": all_events_with_status,
        # List of all events for the calendar
        "filter_status": filter_status,
    }
    return render(request, "accounts/dashboard.html", context)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            # Create a UserProfile if it does not exist
            UserProfile.objects.get_or_create(user=user)

            # Automatically log the user in
            user = authenticate(
                username=user.username, password=form.cleaned_data["password1"]
            )
            if user is not None:
                login(request, user)
                return redirect("dashboard")
    else:
        form = SignupForm()

    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def home(request):
    return render(request, "accounts/home.html")


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        profile_form = ProfilePictureForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            request.user.first_name = request.POST.get("first_name")
            request.user.last_name = request.POST.get("last_name")
            request.user.email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password and password == confirm_password:
                request.user.set_password(
                    password
                )  # Use set_password to hash the password
            elif password and password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("profile")
            request.user.save()
            if password and password == confirm_password:
                request.user.set_password(password)
                messages.success(
                    request,
                    "Profile updated successfully. Please log in again.",
                )
            elif password and password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("profile")
            else:
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
        "date_joined": request.user.date_joined,
        "last_login": request.user.last_login,
        "email": request.user.email,
    }

    context = {
        "user_data": user_data,
        "profile_form": profile_form,
        "view_only": False,
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

    # Redirect with the current search queryS
    search_query = request.GET.get("search_query", "")
    return redirect(
        f"{reverse('friends_page')}?search_query={search_query}",
        search_query=search_query,
    )


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

    # Delete friendships
    friendships = Friendship.objects.filter(
        Q(from_user=current_user, to_user=friend)
        | Q(from_user=friend, to_user=current_user)
    )
    friendships.delete()

    # Delete notifications related to the friend
    Notification.objects.filter(
        Q(user=current_user, event__created_by=friend)
        | Q(user=friend, event__created_by=current_user)
        | Q(
            user=current_user,
            type="friend_request_received",
            event__isnull=True,
        )
        | Q(user=friend, type="friend_request_received", event__isnull=True)
        | Q(
            user=current_user,
            type="suggested_alternate_date",
            event__isnull=False,
            message__icontains=friend.username,
        )
        | Q(
            user=friend,
            type="suggested_alternate_date",
            event__isnull=False,
            message__icontains=current_user.username,
        )
        | Q(
            user=current_user,
            type__in=[
                "event_created",
                "event_updated",
                "event_cancelled",
                "event_confirmed",
                "invitation_response",
            ],
            event__created_by=friend,
        )
        | Q(
            user=friend,
            type__in=[
                "event_created",
                "event_updated",
                "event_cancelled",
                "event_confirmed",
                "invitation_response",
            ],
            event__created_by=current_user,
        )
    ).delete()

    # Delete invitations involving the friend
    invitations = Invitation.objects.filter(
        Q(user=friend) | Q(event__created_by=friend)
    )
    invitations.delete()

    messages.success(
        request, "Friend and all associated data deleted successfully."
    )
    return redirect("friends_page")


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_profile(request, user_id):
    friend_profile = get_object_or_404(UserProfile, user__id=user_id)
    friend_user = friend_profile.user  # Retrieve User object from UserProfile
    context = {
        "user_data": {
            "username": friend_user.username,
            "first_name": friend_user.first_name,
            "last_name": friend_user.last_name,
            "profile_picture": friend_profile.profile_picture,
            "date_joined": friend_user.date_joined,
            "last_login": friend_user.last_login,
            "email": friend_user.email,
        },
        "view_only": request.user.id != user_id,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been deleted successfully.")
    return redirect(
        "home"
    )  # Redirect to the home page or any other page after deletion
