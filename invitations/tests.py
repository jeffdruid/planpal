from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from events.models import Event
from invitations.models import Invitation
from accounts.models import UserProfile, Friendship
from django.utils import timezone


class InvitationsTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password="password",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="password",
        )
        self.client = Client()
        self.client.login(username="testuser1", password="password")

        # Ensure the UserProfiles are created only if they don't exist
        self.profile1, created = UserProfile.objects.get_or_create(
            user=self.user1
        )
        self.profile2, created = UserProfile.objects.get_or_create(
            user=self.user2
        )

        # Create an event
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            proposed_date=timezone.now() + timezone.timedelta(days=1),
            location="Test Location",
            created_by=self.user1,
        )

        # Create a friendship
        self.friendship = Friendship.objects.create(
            from_user=self.user1, to_user=self.user2, status="accepted"
        )

    def test_manage_invitations_view(self):
        """Test to ensure the manage invitations view loads correctly for the event creator."""
        print("Testing manage invitations view...")
        response = self.client.get(
            reverse("manage_invitations", args=[self.event.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "invitations/manage_invitations.html"
        )
        print("Manage invitations view tested successfully.")

    def test_manage_invitations_view_redirect(self):
        """Test to ensure the manage invitations view redirects for non-event creator."""
        print(
            "Testing manage invitations view redirect for non-event creator..."
        )
        self.client.login(username="testuser2", password="password")
        response = self.client.get(
            reverse("manage_invitations", args=[self.event.id])
        )
        self.assertRedirects(response, reverse("dashboard"))
        print("Manage invitations view redirect tested successfully.")

    def test_create_invitation_view(self):
        """Test to ensure the create invitation view loads correctly for the event creator."""
        print("Testing create invitation view...")
        response = self.client.get(
            reverse("create_invitation", args=[self.event.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "invitations/create_invitation.html")
        print("Create invitation view tested successfully.")

    def test_create_invitation_view_redirect(self):
        """Test to ensure the create invitation view redirects for non-event creator."""
        print(
            "Testing create invitation view redirect for non-event creator..."
        )
        self.client.login(username="testuser2", password="password")
        response = self.client.get(
            reverse("create_invitation", args=[self.event.id])
        )
        self.assertRedirects(
            response, reverse("event_details", args=[self.event.id])
        )
        print("Create invitation view redirect tested successfully.")

    def test_create_invitation(self):
        """Test to ensure an invitation is created correctly for a friend."""
        print("Testing create invitation for a friend...")
        response = self.client.post(
            reverse("create_invitation", args=[self.event.id]),
            {"user_id": self.user2.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Invitation.objects.filter(
                event=self.event, user=self.user2
            ).exists()
        )
        print("Create invitation for a friend tested successfully.")

    def test_create_invitation_no_friends(self):
        """Test to ensure a message is shown if there are no friends to invite."""
        print("Testing create invitation with no friends...")
        Friendship.objects.all().delete()
        response = self.client.get(
            reverse("create_invitation", args=[self.event.id])
        )
        self.assertRedirects(response, reverse("friends_page"))
        print("Create invitation with no friends tested successfully.")

    def test_create_invitation_non_friend(self):
        """Test to ensure inviting non-friends is prevented."""
        print("Testing create invitation for a non-friend...")
        user3 = User.objects.create_user(
            username="testuser3",
            email="testuser3@example.com",
            password="password",
        )
        response = self.client.post(
            reverse("create_invitation", args=[self.event.id]),
            {"user_id": user3.id},
        )
        self.assertRedirects(
            response, reverse("create_invitation", args=[self.event.id])
        )
        self.assertFalse(
            Invitation.objects.filter(event=self.event, user=user3).exists()
        )
        print("Create invitation for a non-friend tested successfully.")

    def test_create_invitation_duplicate(self):
        """Test to ensure duplicate invitations are prevented."""
        print("Testing create duplicate invitation...")
        Invitation.objects.create(
            event=self.event, user=self.user2, status="Pending"
        )
        response = self.client.post(
            reverse("create_invitation", args=[self.event.id]),
            {"user_id": self.user2.id},
        )
        self.assertRedirects(
            response, reverse("create_invitation", args=[self.event.id])
        )
        self.assertEqual(
            Invitation.objects.filter(
                event=self.event, user=self.user2
            ).count(),
            1,
        )
        print("Create duplicate invitation tested successfully.")
