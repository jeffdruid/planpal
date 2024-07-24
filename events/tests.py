from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from events.models import Event
from invitations.models import Invitation
from notifications.models import Notification
from django.utils import timezone
from .forms import EventForm


class EventsTestCase(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password",
        )
        self.client = Client()
        self.client.login(username="testuser", password="password")

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

    def test_create_event_view(self):
        """Test to ensure the create event view works correctly."""
        print("Testing create event view...")
        response = self.client.post(
            reverse("create_event"),
            {
                "title": "New Event",
                "description": "This is a new event",
                "location": "New Location",
                "proposed_date": timezone.now() + timezone.timedelta(days=2),
                "status": "Pending",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Check if the status code is 302 (redirect)
        print("Create event view tested successfully.")

    def test_edit_event_view(self):
        """Test to ensure the edit event view works correctly."""
        print("Testing edit event view...")
        response = self.client.post(
            reverse("edit_event", args=[self.event.id]),
            {
                "title": "Updated Event",
                "description": "This is an updated event",
                "location": "Updated Location",
                "proposed_date": timezone.now() + timezone.timedelta(days=3),
                "status": "Confirmed",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Check if the status code is 302 (redirect)
        self.event.refresh_from_db()
        self.assertEqual(
            self.event.title, "Updated Event"
        )  # Check if the event title is updated
        print("Edit event view tested successfully.")

    def test_event_details_view(self):
        """Test to ensure the event details view loads correctly."""
        print("Testing event details view...")
        response = self.client.get(
            reverse("event_details", args=[self.event.id])
        )
        self.assertEqual(
            response.status_code, 200
        )  # Check if the status code is 200 (OK)
        self.assertTemplateUsed(
            response, "events/event_details.html"
        )  # Check if the correct template is used
        print("Event details view tested successfully.")

    def test_delete_event_view(self):
        """Test to ensure the delete event view works correctly."""
        print("Testing delete event view...")
        response = self.client.post(
            reverse("delete_event", args=[self.event.id])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Check if the status code is 302 (redirect)
        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(id=self.event.id)  # Ensure the event is deleted
        print("Delete event view tested successfully.")

    def test_event_form_initial_data(self):
        """Test to ensure the event form is initialized with correct default data."""
        print("Testing event form initial data...")
        form = EventForm()
        self.assertEqual(form.fields["title"].initial, "Default Title")
        self.assertEqual(
            form.fields["description"].initial, "Default Description"
        )
        self.assertEqual(
            form.fields["location"].initial, "The Spire of Dublin"
        )
        self.assertTrue(form.fields["proposed_date"].initial > timezone.now())
        print("Event form initial data tested successfully.")

    def test_event_form_clean_proposed_date(self):
        """Test to ensure the proposed date validation works correctly."""
        print("Testing event form clean proposed date...")
        form_data = {
            "title": "Test Event",
            "description": "This is a test event",
            "location": "Test Location",
            "proposed_date": timezone.now()
            - timezone.timedelta(days=1),  # Past date
            "status": "Pending",
        }
        form = EventForm(data=form_data)
        self.assertFalse(
            form.is_valid()
        )  # The form should be invalid due to past date
        self.assertIn(
            "The proposed date cannot be in the past.",
            form.errors["proposed_date"],
        )
        print("Event form clean proposed date tested successfully.")
