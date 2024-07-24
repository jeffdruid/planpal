from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from notifications.models import Notification
from events.models import Event
from django.utils import timezone


class NotificationsTestCase(TestCase):
    def setUp(self):
        # Set up the initial data for the tests
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

        # Create an event
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            proposed_date=timezone.now() + timezone.timedelta(days=1),
            location="Test Location",
            created_by=self.user1,
        )

        # Create notifications
        self.notification1 = Notification.objects.create(
            user=self.user1,
            event=self.event,
            type="event_created",
            message="A new event 'Test Event' has been created.",
            created_at=timezone.now(),
            read=False,  # Unread notification
        )
        self.notification2 = Notification.objects.create(
            user=self.user1,
            event=self.event,
            type="event_updated",
            message="The event 'Test Event' has been updated.",
            created_at=timezone.now(),
            read=True,  # Read notification
        )
        self.notification3 = Notification.objects.create(
            user=self.user1,
            type="friend_request_received",
            message="You have a new friend request.",
            created_at=timezone.now(),
            read=False,  # Unread notification
        )

    def test_notifications_view(self):
        """Test to ensure the notifications view loads correctly."""
        print("Testing notifications view...")
        response = self.client.get(reverse("notifications"))
        self.assertEqual(
            response.status_code, 200
        )  # Check if the view loads successfully
        self.assertTemplateUsed(
            response, "notifications/notifications.html"
        )  # Check if the correct template is used
        print("Notifications view tested successfully.")

    def test_mark_notification_read(self):
        """Test to ensure a notification is marked as read and redirects correctly."""
        print("Testing mark notification as read...")

        # Mark an event notification as read
        response = self.client.get(
            reverse("mark_notification_read", args=[self.notification1.id])
        )
        self.notification1.refresh_from_db()
        self.assertTrue(
            self.notification1.read
        )  # Check if the notification is marked as read
        self.assertRedirects(
            response, reverse("event_details", args=[self.event.id])
        )  # Check if it redirects correctly
        print("Mark notification as read for event tested successfully.")

        # Mark a friend request notification as read
        response = self.client.get(
            reverse("mark_notification_read", args=[self.notification3.id])
        )
        self.notification3.refresh_from_db()
        self.assertTrue(
            self.notification3.read
        )  # Check if the notification is marked as read
        self.assertRedirects(
            response, reverse("friends_page")
        )  # Check if it redirects correctly
        print(
            "Mark notification as read for friend request tested successfully."
        )

    def test_get_notifications(self):
        """Test to ensure unread notifications are fetched correctly."""
        print("Testing get notifications...")
        response = self.client.get(reverse("get_notifications"))
        self.assertEqual(
            response.status_code, 200
        )  # Check if the request is successful
        self.assertEqual(
            response.json()["unread_count"], 2
        )  # Check if the unread count is correct
        self.assertEqual(
            len(response.json()["notifications"]), 2
        )  # Check if the correct number of notifications are returned
        print("Get notifications tested successfully.")
