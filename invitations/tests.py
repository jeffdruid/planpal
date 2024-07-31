from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from events.models import Event
from invitations.models import Invitation
from accounts.models import UserProfile, Friendship
from notifications.models import Notification
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
        self.user3 = User.objects.create_user(
            username="testuser3",
            email="testuser3@example.com",
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
        self.profile3, created = UserProfile.objects.get_or_create(
            user=self.user3
        )

        # Create an event
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            proposed_date=timezone.now() + timezone.timedelta(days=1),
            location="Test Location",
            created_by=self.user1,
        )

        # Create friendships
        self.friendship1 = Friendship.objects.create(
            from_user=self.user1, to_user=self.user2, status="accepted"
        )
        self.friendship2 = Friendship.objects.create(
            from_user=self.user1, to_user=self.user3, status="accepted"
        )

    def test_invalid_event_id(self):
        """Test to ensure view handles invalid event ID gracefully."""
        response = self.client.get(reverse("manage_invitations", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_invalid_user_id(self):
        """Test to ensure view handles invalid user ID gracefully."""
        response = self.client.post(
            reverse("create_invitation", args=[self.event.id]),
            {"user_id": 999},
        )
        self.assertEqual(response.status_code, 404)

    def test_notification_creation(self):
        """
        Test to ensure notifications are created
        when invitations are sent.
        """
        self.client.post(
            reverse("create_invitation", args=[self.event.id]),
            {"user_id": self.user2.id},
        )
        notification = Notification.objects.filter(
            user=self.user2, event=self.event, type="event_created"
        ).first()
        self.assertIsNotNone(notification)

    def test_bulk_invitation_sending(self):
        """Test to ensure all friends can be invited at once."""
        self.client.post(
            reverse("create_invitation", args=[self.event.id]),
            {"send_all": "1"},
        )
        invitations = Invitation.objects.filter(event=self.event)
        self.assertEqual(invitations.count(), 2)
        self.assertTrue(
            Invitation.objects.filter(
                event=self.event, user=self.user2
            ).exists()
        )
        self.assertTrue(
            Invitation.objects.filter(
                event=self.event, user=self.user3
            ).exists()
        )

    def test_authorization_for_non_event_creator(self):
        """Test to ensure non-event creators cannot send invitations."""
        self.client.login(username="testuser2", password="password")
        response = self.client.post(
            reverse("create_invitation", args=[self.event.id]),
            {"user_id": self.user3.id},
        )
        self.assertRedirects(
            response, reverse("event_details", args=[self.event.id])
        )
        self.assertFalse(
            Invitation.objects.filter(
                event=self.event, user=self.user3
            ).exists()
        )
