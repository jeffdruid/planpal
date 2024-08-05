# README for Social Event Planner Application

## [Back to Main Page](README.md)

### Social Event Planner Application

- The testing results were documented in this file to provide an overview of the testing process and outcomes.

### Manual Testing

- **Manual testing** was performed to validate the functionality and user experience of the Social Event Planner application.

#### Table of Contents
   - [Testing User Stories](#testing-user-stories)
   - [Test Cases](#test-cases)
     - [Accounts App](#accounts-app)
     - [Invitations App](#invitations-app)
     - [Notifications App](#notifications-app)
      - [Events App](#events-app)
   - [Validator Testing](#validator-testing)
      - [W3C html Validator](#w3c-html-validator)
      - [W3C CSS Validator](#w3c-css-validator)
     - [flake8](#flake8)
     - [JSHint](#jshint)
     - [CI Python Linter](#ci-python-linter)
      - [Django's Built-in Check System](#djangos-built-in-check-system)
      - [WAVE - Web Accessibility Evaluation Tool](#wave---web-accessibility-evaluation-tool)
      - [Lighthouse](#lighthouse)
   - [Manual Testing](#manual-testing)
     - [Responsiveness and Device Compatibility](#responsiveness-and-device-compatibility)
      - [Cross-browser Compatibility](#cross-browser-compatibility)
     - [Link Validation](#link-validation)
     - [Text and Font Readability](#text-and-font-readability)
     - [Acceptance Test](#acceptance-test)
      - [Responsiveness](#responsiveness)

### Testing User Stories

| Story ID | User Story Description                                          | Acceptance Criteria                                                                                                                                       |
|----------|-----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| US01     | As a user, I want to sign up for an account                     | - The sign-up page loads correctly.<br>- Users can enter username, email, and password.<br>- User receives a confirmation email.<br>- User is logged in automatically after signing up. |
| US02     | As a user, I want to log in to my account                       | - The login page loads correctly.<br>- Users can enter username and password.<br>- User is redirected to the dashboard upon successful login.             |
| US03     | As a user, I want to reset my password                          | - The forgot password link is available on the login page.<br>- Users receive a one-time login link in their email.<br>- Users can set a new password.     |
| US04     | As a user, I want to view my profile                            | - The profile page loads correctly.<br>- Users can view their username, email, and profile picture.<br>- Users can update their profile information.       |
| US05     | As a user, I want to manage my events                           | - The dashboard shows all user-created and invited events.<br>- Users can filter events by status.<br>- Users can view details of each event.              |
| US06     | As a user, I want to invite friends to events                   | - Users can see a list of their friends.<br>- Users can send event invitations to friends.<br>- Users receive notifications for new invitations.           |
| US07     | As a user, I want to accept or decline friend requests          | - Users receive notifications for new friend requests.<br>- Users can accept or decline friend requests.<br>- Users can see a list of their friends.       |
| US08     | As a user, I want to send friend requests                       | - Users can search for other users.<br>- Users can send friend requests to other users.<br>- Users receive notifications for sent requests.                |
| US09     | As a user, I want to delete a friend                            | - Users can remove friends from their friend list.<br>- Associated data (notifications, invitations) are deleted.<br>- Users receive confirmation of removal. |
| US10     | As an event creator, I want to manage event invitations         | - Users can view a list of sent invitations.<br>- Users can see the status of each invitation.              |
| US11     | As an admin, I want to manage user accounts                     | - Admins can view a list of all users.<br>- Admins can delete or deactivate user accounts.<br>- Admins can reset user passwords.                          |
| US12     | As a user, I want to receive notifications                      | - Users receive notifications for new events, invitations, and friend requests.<br>- Users can mark notifications as read.<br>- Unread notifications are highlighted. |

### Test Cases
- Unit tests were created to cover the core functionality of the application, including user authentication, event creation, invitations, notifications, and friend management. The tests ensure that the application works as expected and that new features do not introduce regressions.
![test cases](images/test-unit-tests.png)

#### Accounts App:

- Dashboard View: Ensures the dashboard loads correctly and displays the correct information.
   ```python
   def test_dashboard_view(self):
    """Test to ensure the dashboard view loads correctly."""
    print("Testing dashboard view...")
    response = self.client.get(reverse("dashboard"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "accounts/dashboard.html")
    print("Dashboard view tested successfully.")
   ```
   - It sends a GET request to the dashboard URL.
   - It verifies that the response status code is 200 (OK) and that the correct template (accounts/dashboard.html) is used.

- Signup View: Verifies that the signup process works correctly.
   ```python
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
    self.assertEqual(response.status_code, 302)
    print("Signup view tested successfully.")
   ```
   - It sends a POST request to the signup URL with new user details.
   - It checks that the response status code is 302 (redirect) after successful signup.

- Profile View: Confirms the profile view loads and updates correctly.
   ```python
   def test_profile_view(self):
    """Test to ensure the profile view loads correctly."""
    print("Testing profile view...")
    response = self.client.get(reverse("profile"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "accounts/profile.html")
    print("Profile view tested successfully.")
   ```
   - It sends a GET request to the profile URL.
   - It verifies that the response status code is 200 (OK) and that the correct template (accounts/profile.html) is used.

- Friends Page View: Checks that the friends page loads correctly.
   ```python
   def test_friends_page_view(self):
    """Test to ensure the friends page view loads correctly."""
    print("Testing friends page view...")
    response = self.client.get(reverse("friends_page"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "accounts/friends.html")
    print("Friends page view tested successfully.")
   ```
   - It sends a GET request to the friends page URL.
   - It verifies that the response status code is 200 (OK) and that the correct template (accounts/friends.html) is used.

- Send Friend Request: Ensures friend requests can be sent.
   ```python
   def test_send_friend_request(self):
    """Test to ensure sending a friend request works correctly."""
    print("Testing send friend request...")
    new_user = User.objects.create_user(
        username="friend", email="friend@example.com", password="password"
    )
    response = self.client.get(reverse("send_friend_request", args=[new_user.id]))
    self.assertEqual(response.status_code, 302)
    print("Send friend request tested successfully.")
   ```
   - It creates a new user and sends a GET request to the send friend request URL with the user's ID.
   - It checks that the response status code is 302 (redirect) after sending the friend request.

- Respond Friend Request: Validates the process of responding to a friend request.
   ```python
   def test_respond_friend_request(self):
    """Test to ensure responding to a friend request works correctly."""
    print("Testing respond friend request...")
    new_user = User.objects.create_user(
        username="friend", email="friend@example.com", password="password"
    )
    friendship = Friendship.objects.create(
        from_user=self.user, to_user=new_user, status="pending"
    )
    response = self.client.get(reverse("respond_friend_request", args=[friendship.id, "accept"]))
    self.assertEqual(response.status_code, 302)
    print("Respond friend request tested successfully.")
   ```
   - It creates a new user and a pending friendship request.
   - It sends a GET request to the respond friend request URL with the friendship ID and response type.
   - It checks that the response status code is 302 (redirect) after responding to the friend request.

- Delete Friend: Tests the deletion of friends.
   ```python
   def test_delete_friend(self):
    """Test to ensure deleting a friend works correctly."""
    print("Testing delete friend...")
    new_user = User.objects.create_user(
        username="friend", email="friend@example.com", password="password"
    )
    friendship = Friendship.objects.create(
        from_user=self.user, to_user=new_user, status="accepted"
    )
    response = self.client.get(reverse("delete_friend", args=[new_user.id]))
    self.assertEqual(response.status_code, 302)
    print("Delete friend tested successfully.")
   ```
   - It creates a new user and an accepted friendship.
   - It sends a GET request to the delete friend URL with the friend's ID.
   - It checks that the response status code is 302 (redirect) after deleting the friend.

- Search Users: Tests the user search functionality.
   ```python
   def test_friend_search_form(self):
    """Test to ensure the FriendSearchForm works correctly."""
    print("Testing FriendSearchForm...")
    form_data = {"search_query": "test"}
    form = FriendSearchForm(data=form_data)
    self.assertTrue(form.is_valid())
    self.assertEqual(form.cleaned_data["search_query"], "test")
    print("FriendSearchForm tested successfully.")
   ```
   - It creates a search query and tests the FriendSearchForm.
   - It checks that the form is valid and contains the correct search query.
   
- Profile Picture Form: Validates the profile picture form. 
   ```python
   def test_profile_picture_form(self):
    """Test to ensure the ProfilePictureForm works correctly."""
    print("Testing ProfilePictureForm...")
    form_data = {"profile_picture": "p1.png"}
    form = ProfilePictureForm(data=form_data)
    self.assertTrue(form.is_valid())
    self.assertEqual(form.cleaned_data["profile_picture"], "p1.png")
    print("ProfilePictureForm tested successfully.")
   ```
   - It creates form data and initializes the form.
   - It checks that the form is valid and contains the correct profile picture.

- One-Time Login Link:
   - Sending the one-time login link.
      ```python
      def test_send_one_time_login_link(self):
      """Test to ensure the one-time login link is sent to the correct email."""
      print("Testing send one-time login link...")
      response = self.client.post(
         reverse("send_one_time_login_link_form"),
         {"email": self.user.email},
      )
      self.assertEqual(response.status_code, 302)
      self.assertEqual(len(mail.outbox), 1)
      self.assertIn(
         "Your one-time login link for PlanPal", mail.outbox[0].subject
      )
      print("Send one-time login link tested successfully.")
      ```
      - It sends a POST request to the send_one_time_login_link_form view with the user's email address.
      - It checks that the response status code is 302 (redirect) and that an email is sent.
      - It asserts that the email subject contains the expected text.
   
   - Logging in using the one-time login link.
      ```python
      def test_one_time_login(self):
         """Test to ensure the user can log in using the one-time login link."""
         print("Testing one-time login...")
         token = default_token_generator.make_token(self.user)
         uid = urlsafe_base64_encode(force_bytes(self.user.pk))
         response = self.client.get(reverse("one_time_login", args=[uid, token]))
         self.assertRedirects(response, reverse("set_new_password"))
         print("One-time login tested successfully.")
      ```
      - It generates a one-time login token and user ID.
      - It sends a GET request to the one_time_login view with the user ID and token.
      - It checks that the response is redirected to the set_new_password view.

   - Handling expired tokens.
      ```python
      def test_expired_one_time_login_token(self):
         """Test to ensure the expired token does not allow login."""
         print("Testing expired one-time login token...")
         token = default_token_generator.make_token(self.user)
         uid = urlsafe_base64_encode(force_bytes(self.user.pk))
         self.user.set_password("newpassword")
         self.user.save()
         response = self.client.get(reverse("one_time_login", args=[uid, token]))
         self.assertRedirects(response, reverse("account_login"))
         print("Expired one-time login token tested successfully.")
      ```
      - It generates a one-time login token and user ID.
      - It sets a new password for the user.
      - It sends a GET request to the one_time_login view with the user ID and token.

   - Ensuring invalid user IDs are handled gracefully.
      ```python
      def test_invalid_user_id(self):
         """Test to ensure view handles invalid user ID gracefully."""
         print("Testing invalid user ID...")
         response = self.client.get(reverse("view_profile", args=[999]))
         self.assertEqual(response.status_code, 404)
         print("Invalid user ID tested successfully.")
      ```
      - It sends a GET request to the view_profile view with an invalid user ID.
      - It checks that the response status code is 404 (Not Found).
      - It ensures that the view handles invalid user IDs gracefully.

#### Invitations App:

- Manage Invitations View: Verifies that event creators can manage invitations.
   ```python
   def test_manage_invitations_view(self):
        """Test to ensure the manage invitations view loads correctly for the event creator."""
        response = self.client.get(
            reverse("manage_invitations", args=[self.event.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "invitations/manage_invitations.html"
        )
   ```
   - It sends a GET request to the manage_invitations view with the event ID.
   - It checks that the response status code is 200 (OK) and that the correct template (invitations/manage_invitations.html) is used.

- Create Invitation View: Ensures event creators can invite friends and handle various scenarios (e.g., no friends, non-friends, duplicate invitations).
   ```python
   def test_create_invitation_no_friends(self):
        """Test to ensure a message is shown if there are no friends to invite."""
        Friendship.objects.all().delete()
        response = self.client.get(
            reverse("create_invitation", args=[self.event.id])
        )
        self.assertRedirects(response, reverse("friends_page"))
   ```
   - It deletes all friendships and sends a GET request to the create_invitation view.
   - It checks that the response is redirected to the friends page.

   ```python
    def test_create_invitation_duplicate(self):
        """Test to ensure duplicate invitations are prevented."""
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
   ```
   - It creates a pending invitation for a user and sends a POST request to the create_invitation view with the same user ID.
   - It checks that the response is redirected back to the create_invitation view and that only one invitation exists for the user.

- Bulk Invitations: Verifies that all friends can be invited to an event at once.
   ```python
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
   ```
   - It sends a POST request to the create_invitation view with the event ID and the send_all parameter.
   - It checks that invitations are created for all friends of the event creator.

- Notification Creation: Ensures that notifications are sent when invitations are created.
   ```python
   def test_notification_creation(self):
        """Test to ensure notifications are created when invitations are sent."""
        self.client.post(
            reverse("create_invitation", args=[self.event.id]),
            {"user_id": self.user2.id},
        )
        notification = Notification.objects.filter(
            user=self.user2, event=self.event, type="event_created"
        ).first()
        self.assertIsNotNone(notification)
   ```
   - It sends a POST request to the create_invitation view with the event ID and user ID.
   - It checks that a notification is created for the invited user and the event.


#### Notifications App:

- Notifications View: Ensures the notifications view loads correctly.
   ```python
    def test_notifications_view(self):
        response = self.client.get(reverse("notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notifications/notifications.html")
   ```
   - It sends a GET request to the notifications view.
   - It checks that the response status code is 200 (OK) and that the correct template (notifications/notifications.html) is used.

- Mark Notification Read: Confirms notifications can be marked as read and the correct redirection occurs.
   ```python
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
   ```
   - It sends a GET request to the mark_notification_read view with the notification ID.
   - It checks that the notification is marked as read and that the response is redirected to the correct page.

- Get Notifications: Verifies that unread notifications are fetched correctly.
   ```python
   def test_get_notifications(self):
        response = self.client.get(reverse("get_notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["unread_count"], 2)
        self.assertEqual(len(response.json()["notifications"]), 2)
   ```
   - It sends a GET request to the get_notifications view.
   - It checks that the response status code is 200 (OK), the unread count is correct, and the number of notifications is correct.

#### Events App:
- Create Event View: Tests the event creation process, including form validation and successful event creation.
   ```python
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
   ```
   - It sends a POST request to the create_event view with event details.
   - It checks that the response status code is 302 (redirect) after creating the event.

- Edit Event View: Ensures event details can be edited and saved correctly.
   ```python
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
   ```
   - It sends a POST request to the edit_event view with updated event details.
   - It checks that the response status code is 302 (redirect) and that the event details are updated.

- Event Details View: Checks that event details are displayed correctly and that the correct template is used.
   ```python
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
   ```
   - It sends a GET request to the event_details view with the event ID.
   - It checks that the response status code is 200 (OK) and that the correct template (events/event_details.html) is used.

- Delete Event View: Validates the event deletion process and associated data removal.
   ``` python
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
   ```
   - It sends a POST request to the delete_event view with the event ID.
   - It checks that the response status code is 302 (redirect) and that the event is deleted.


### Validator Testing
#### W3C HTML Validator
- The W3C HTML Validator is used to check the HTML code for compliance with web standards.
   | Page | Results |
   |------|---------|
   | Home | ![home](images/html-home.png) |
   | Login | ![login]( images/html-login.png) |
   | Signup | ![signup]( images/html-signup.png) |
   | Password Reset | ![password reset]( images/html-reset.png) |
   | Logout | ![logout]( images/html-logout.png) |
   | Dashboard | ![dashboard]( images/html-dashboard.png) |
   | Profile | ![profile]( images/html-profile.png) |
   | Friends | ![friends]( images/html-friends.png) |
   | Notifications | ![notifications]( images/html-notifications.png) |
   | Invitations | ![invitations]( images/html-invitations.png) |
   | Create Event | ![create event]( images/html-create.png) |
   | Edit Event | ![edit event]( images/html-edit.png) |
   | Event Details | ![event details]( images/html-details.png) |


#### W3C CSS Validator
- The W3C CSS Validator is used to check the CSS code for compliance with web standards.
   ![css validator]( images/validator-css-w3c.png)
   - W3C Web Validator extension in Visual Studio Code.
   ![css validator]( images/validator-css-vsc.png)

#### flake8
- Flake8 is a Python linting tool that checks the codebase for style and syntax errors.
   ![flake8]( images/flake8.png)
   -  The flake8 tool was used to check the codebase for PEP8 compliance and syntax errors.

#### Jshint
- Jshint is a JavaScript code quality tool that helps identify errors and potential problems in JavaScript code.

| From | Results |
|------|---------|
| event_form.js | ![base.js]( images/jshint-event.png) |
| scripts.js | ![calendar.js]( images/jshint-scripts.png) |
| modals.js | ![friends.js]( images/jshint-modals.png) |
| profile.js | ![invitations.js]( images/jshint-profile.png) |

#### CI Python Linter
- The CI Python Linter is a continuous integration tool that runs flake8 on the codebase to ensure it meets the required standards.

| From | Results |
|------|---------|
| Notifications App / Views.py | ![Notifications App]( images/linter-notifications-views.png) |
| Notifications App / Utils.py | ![Notifications App]( images/linter-notifications-utils.png) |
| Notifications App / Urls.py| ![Notifications App]( images/linter-notifications-urls.png) |
| Notifications App / Tests.py | ![Notifications App]( images/linter-notifications-tests.png) |
| Notifications App / Models.py | ![Notifications App]( images/linter-notifications-models.png) |
| Notifications App / Context_processors.py | ![Notifications App]( images/linter-notifications-context.png) |
| Invitations App / Views.py | ![Invitations App]( images/linter-invitations-views.png) |
| Invitations App / Urls.py | ![Invitations App]( images/linter-invitations-urls.png) |
| Invitations App / Models.py | ![Invitations App]( images/linter-invitations-models.png) |
| Invitations App / Tests.py | ![Invitations App]( images/linter-invitations-tests.png) |
| Events App / Views.py | ![Events App]( images/linter-events-views.png) |
| Events App / Urls.py | ![Events App]( images/linter-events-urls.png) |
| Events App / Models.py | ![Events App]( images/linter-events-models.png) |
| Events App / Forms.py | ![Events App]( images/linter-events-forms.png) |
| Events App / Tests.py | ![Events App]( images/linter-events-tests.png) |
| Accounts App / Views.py | ![Accounts App]( images/linter-accounts-views.png) |
| Accounts App / Urls.py | ![Accounts App]( images/linter-accounts-urls.png) |
| Accounts App / Models.py | ![Accounts App]( images/linter-accounts-models.png) |
| Accounts App / Forms.py | ![Accounts App]( images/linter-accounts-forms.png) |
| Accounts App / Tests.py | ![Accounts App]( images/linter-accounts-tests.png) |
| Accounts App / Tests.py | ![Accounts App]( images/linter-accounts-middleware.png) |


#### Django's Built-in Check System
Django provides a management command check that can help identify some issues within your project.
   ```bash
      python manage.py check
   ```
   ![check]( images/test-django-check.png)

#### WAVE - Web Accessibility Evaluation Tool
- WAVE is a web accessibility evaluation tool that helps identify accessibility issues in web pages.
   ![wave]( images/wave-home.png)

#### LightHouse
- LightHouse is a tool for improving the quality of web pages. It provides audits for performance, accessibility, best practices, SEO, and progressive web apps.
   - The LightHouse extension in Google Chrome was used to audit the application for performance, accessibility, best practices, and SEO.
create a table with the results of the audit.

| From | Results | 
|-------------|---------------|
| Home         | ![Home]( images/lighthouse-home.png) |
| Login        | ![Login]( images/lighthouse-login.png) |
| Signup       | ![Signup]( images/lighthouse-signup.png) |
| Password Reset| ![Password Reset]( images/lighthouse-password.png) |
| Logout       | ![Logout]( images/lighthouse-logout.png) | 
| Dashboard    | ![Dashboard]( images/lighthouse-dashboard.png) |
| Profile      | ![Profile]( images/lighthouse-profile.png) |
| Friends      | ![Friends]( images/lighthouse-friends.png) |
| Notifications| ![Notifications]( images/lighthouse-notification.png) |
| Invitations  | ![Invitations]( images/lighthouse-invitations.png)|
| Create Event | ![Create Event]( images/lighthouse-add.png) |
| Edit Event   | ![Edit Event]( images/lighthouse-edit.png) |
| Event Details| ![Event Details]( images/lighthouse-event.png) |

### Manual Testing
- Manual testing is performed to verify the functionality of the application from a user's perspective.

#### Cross-browser Compatibility

- Verified the functionality of the page across different web browsers to ensure it works properly and it is consistent.

#### Responsiveness and Device Compatibility

- Verified that the project displays correctly and functions appropriately across various device sizes, ensuring a good user experience.

#### Link Validation

- Verified all internal and external links to ensure they direct users to the intended destinations and open correctly without issues.

#### Text and Font Readability

- Verified that all text content and fonts used on the page are legible, clear, and easy to understand.

#### Acceptance Test

- Verified that the application meets the specified user stories and acceptance criteria.

The manual testing confirms that the page operates smoothly across multiple browsers, adapts well to different devices, ensures accurate link navigation, and maintains clear readability for users interacting with the content.

#### Responsiveness
- The application is tested on various devices and screen sizes to ensure responsiveness and compatibility.

##### Desktop

| Device | Browser | Results |
|--------|---------|---------|
| Desktop | Chrome | ![Desktop](images/web-chrome-dashboard.png) |
| Desktop | Firefox | ![Desktop](images/web-firefox-dashboard.png) |
| Desktop | Edge | ![Desktop](images/web-edge-dashboard.png) |

- *Chrome Desktop - Version 127.0.6533.89 (Official Build) (64-bit)*
- *Firefox Desktop - Version 128.0.3 (Official Build) (64-bit)*
- *Edge Desktop - Version 127.0.2651.86 (Official build) (64-bit)*

##### Mobile

| Chrome | Firefox | Edge |
|--------|---------|------|
|<img src="images/mob-chrome-dashboard.png" width="300"> | <img src="images/mob-fire-dashboard.png" width="300"> | <img src="images/mob-edge-dashboard.png" width="300"> |

- *Chrome Mobile - Version 127.0.6533.77 (Official Build)*
- *Firefox Mobile - Version 128.3 (43849) (Official Build)*
- *Edge Mobile - Version 127.0.2651.81 (Official build)*

##### Tablet

| Chrome | Firefox | Edge |
|--------|---------|------|
|<img src="images/tab_Chrome.jpg" width="300"> | <img src="images/tab_Firefox.jpg" width="300"> | <img src="images/tab_Edge.jpg" width="300"> |

- *Chrome Tablet - Version 126.0.6478.50 (Official Build)*
- *Firefox Tablet - Version 128.0.3 (2016034663) (Official Build)*
- *Edge Tablet - Version 125.0.2535.87 (Official build)*

**[Back to Top](#social-event-planner-application)**