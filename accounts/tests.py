from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile, Friendship
from events.models import Event
from invitations.models import Invitation
from django.utils import timezone
from accounts.forms import ProfilePictureForm, FriendSearchForm


class AccountsTestCase(TestCase):
    def setUp(self):
        """Set up the test environment by creating a user and an event."""
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password",
        )
        self.client = Client()
        self.client.login(username="testuser", password="password")

        # Ensure the UserProfile is created only if it doesn't exist
        self.profile, created = UserProfile.objects.get_or_create(
            user=self.user
        )

        # Create an event for testing
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            proposed_date=timezone.now() + timezone.timedelta(days=1),
            location="Test Location",
            created_by=self.user,
        )

        # Create an invitation for testing
        self.invitation = Invitation.objects.create(
            event=self.event, user=self.user, status="pending"
        )

    def test_dashboard_view(self):
        """Test to ensure the dashboard view loads correctly."""
        print("Testing dashboard view...")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(
            response.status_code, 200
        )  # Check if the status code is 200 (OK)
        self.assertTemplateUsed(
            response, "accounts/dashboard.html"
        )  # Check if the correct template is used
        print("Dashboard view tested successfully.")
        print(response.context["upcoming_events_with_read_status"])

    def test_signup_view(self):
        """Test to ensure the signup view works correctly."""
        print("Testing signup view...")
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "newpassword",
                "password2": "newpassword",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Check if the status code is 302 (redirect)
        print("Signup view tested successfully.")

    def test_profile_view(self):
        """Test to ensure the profile view loads correctly."""
        print("Testing profile view...")
        response = self.client.get(reverse("profile"))
        self.assertEqual(
            response.status_code, 200
        )  # Check if the status code is 200 (OK)
        self.assertTemplateUsed(
            response, "accounts/profile.html"
        )  # Check if the correct template is used
        print("Profile view tested successfully.")

    def test_friends_page_view(self):
        """Test to ensure the friends page view loads correctly."""
        print("Testing friends page view...")
        response = self.client.get(reverse("friends_page"))
        self.assertEqual(
            response.status_code, 200
        )  # Check if the status code is 200 (OK)
        self.assertTemplateUsed(
            response, "accounts/friends.html"
        )  # Check if the correct template is used
        print("Friends page view tested successfully.")

    def test_send_friend_request(self):
        """Test to ensure sending a friend request works correctly."""
        print("Testing send friend request...")
        new_user = User.objects.create_user(
            username="friend", email="friend@example.com", password="password"
        )
        response = self.client.get(
            reverse("send_friend_request", args=[new_user.id])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Check if the status code is 302 (redirect)
        print("Send friend request tested successfully.")

    def test_respond_friend_request(self):
        """Test to ensure responding to a friend request works correctly."""
        print("Testing respond friend request...")
        new_user = User.objects.create_user(
            username="friend", email="friend@example.com", password="password"
        )
        friendship = Friendship.objects.create(
            from_user=self.user, to_user=new_user, status="pending"
        )
        response = self.client.get(
            reverse("respond_friend_request", args=[friendship.id, "accept"])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Check if the status code is 302 (redirect)
        print("Respond friend request tested successfully.")

    def test_delete_friend(self):
        """Test to ensure deleting a friend works correctly."""
        print("Testing delete friend...")
        new_user = User.objects.create_user(
            username="friend", email="friend@example.com", password="password"
        )
        friendship = Friendship.objects.create(
            from_user=self.user, to_user=new_user, status="accepted"
        )
        response = self.client.get(
            reverse("delete_friend", args=[new_user.id])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Check if the status code is 302 (redirect)
        print("Delete friend tested successfully.")

    def test_profile_picture_form(self):
        """Test to ensure the ProfilePictureForm works correctly."""
        print("Testing ProfilePictureForm...")
        form_data = {"profile_picture": "p1.png"}
        form = ProfilePictureForm(data=form_data)
        self.assertTrue(
            form.is_valid()
        )  # Form should be valid with correct data
        self.assertEqual(form.cleaned_data["profile_picture"], "p1.png")
        print("ProfilePictureForm tested successfully.")

    def test_friend_search_form(self):
        """Test to ensure the FriendSearchForm works correctly."""
        print("Testing FriendSearchForm...")
        form_data = {"search_query": "test"}
        form = FriendSearchForm(data=form_data)
        self.assertTrue(
            form.is_valid()
        )  # Form should be valid with correct data
        self.assertEqual(form.cleaned_data["search_query"], "test")
        print("FriendSearchForm tested successfully.")
