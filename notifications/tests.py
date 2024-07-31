from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from notifications.models import Notification
from events.models import Event
from django.utils import timezone


class NotificationsTestCase(TestCase):
    def setUp(self):
        # Set up the initial data for the tests
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

        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            proposed_date=timezone.now() + timezone.timedelta(days=1),
            location="Test Location",
            created_by=self.user1,
        )

        self.notification1 = Notification.objects.create(
            user=self.user1,
            event=self.event,
            type="event_created",
            message="A new event 'Test Event' has been created.",
            created_at=timezone.now(),
            read=False,
        )
        self.notification2 = Notification.objects.create(
            user=self.user1,
            event=self.event,
            type="event_updated",
            message="The event 'Test Event' has been updated.",
            created_at=timezone.now(),
            read=True,
        )
        self.notification3 = Notification.objects.create(
            user=self.user1,
            type="friend_request_received",
            message="You have a new friend request.",
            created_at=timezone.now(),
            read=False,
        )

    def test_notifications_view(self):
        response = self.client.get(reverse("notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notifications/notifications.html")

    def test_mark_notification_read(self):
        response = self.client.get(
            reverse("mark_notification_read", args=[self.notification1.id])
        )
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.read)
        self.assertRedirects(
            response, reverse("event_details", args=[self.event.id])
        )

        response = self.client.get(
            reverse("mark_notification_read", args=[self.notification3.id])
        )
        self.notification3.refresh_from_db()
        self.assertTrue(self.notification3.read)
        self.assertRedirects(response, reverse("friends_page"))

    def test_get_notifications(self):
        response = self.client.get(reverse("get_notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["unread_count"], 2)
        self.assertEqual(len(response.json()["notifications"]), 2)

    def test_mark_nonexistent_notification(self):
        response = self.client.get(
            reverse("mark_notification_read", args=[999])
        )
        self.assertEqual(response.status_code, 404)

    def test_mark_notification_unauthenticated(self):
        self.client.logout()
        response = self.client.get(
            reverse("mark_notification_read", args=[self.notification1.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_access_notifications_of_other_user(self):
        self.client.logout()
        self.client.login(username="testuser2", password="password")
        response = self.client.get(
            reverse("mark_notification_read", args=[self.notification1.id])
        )
        self.assertEqual(response.status_code, 403)  # Should return forbidden
