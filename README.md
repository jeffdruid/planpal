# [PlanPal - Social Event Planner](https://planpal-1fe5e3919654.herokuapp.com/)
<a href="https://planpal-1fe5e3919654.herokuapp.com/">
  <img src="README/images/planpal-banner.png" alt="PlanPal banner" width="100%">
</a>


## Introduction

- Social Event Planner is a web application designed to help users create, manage, and share events with their friends. It provides features for event creation, invitations, notifications, and user profile management.

   ![Dashboard](README/images/dashboard.png)
View the live project [here](https://planpal-1fe5e3919654.herokuapp.com/)

## Table of Contents
1. [Introduction](#introduction)
2. [Technologies Used](#technologies-used)
   - [Django](#django)
   - [SQLite](#sqlite)
   - [Bootstrap](#bootstrap)
   - [jQuery](#jquery)
   - [FullCalendar](#fullcalendar)
   - [Google Places API](#google-places-api)
   - [Font Awesome](#font-awesome)
   - [Ajax](#ajax)
   - [Tippy.js](#tippyjs)
   - [Moment.js](#momentjs)
   - [Heroku](#heroku)
   - [SendGrid](#sendgrid)
3. [User Stories](#user-stories)
   - [User Story 1: User Authentication](#user-story-1-user-authentication)
   - [User Story 2: Event Creation](#user-story-2-event-creation)
   - [User Story 3: Invitation System](#user-story-3-invitation-system)
   - [User Story 4: Availability](#user-story-4-availability)
   - [User Story 5: Friendship System](#user-story-5-friendship-system)
   - [User Story 6: Notification System](#user-story-6-notification-system)
   - [User Story 7: Dashboard](#user-story-7-dashboard)
   - [User Story 8: Profile Management](#user-story-8-profile-management)
4. [Wireframes](#wireframes)
   - [Site Map](#site-map)
   - [Database Schema](#database-schema)
   - [Color Palette](#color-palette)
5. [Features](#features)
   - [User Authentication](#user-authentication)
   - [Event Creation and Management](#event-creation-and-management)
   - [Invitation System](#invitation-system)
   - [Notification System](#notification-system)
   - [Friend Management](#friend-management)
   - [Calendar Integration](#calendar-integration)
   - [Location Services](#location-services)
   - [User Dashboard](#user-dashboard)
   - [Dynamic Data Integration](#dynamic-data-integration)
   - [Error Handling](#error-handling)
   - [Responsive Design](#responsive-design)
   - [Security Features](#security-features)
   - [Additional Features](#additional-features)
6. [MoSCoW Prioritization](#moscow-prioritization)
   - [Must Have](#must-have)
   - [Should Have](#should-have)
   - [Could Have](#could-have)
   - [Won't Have (for now)](#wont-have-for-now)
6. [GitHub Projects, Milestones, and Issues](#github-projects-milestones-and-issues)
   - [GitHub Projects](#github-projects)
   - [Milestones](#milestones)
   - [Issues](#issues)
6. [Troubleshooting](#troubleshooting)
   - [Password Reset](#password-reset)
7. [Testing](#testing)
8. [Bugs](#bugs)
   - [Google Sheets Not Opening in a New Tab (Deployment Issue)](#google-sheets-not-opening-in-a-new-tab-deployment-issue)
   - [Fixed Bugs](#fixed-bugs)
     - [Trail slash in the URL](#trail-slash-in-the-url)
9. [UI Improvements](#ui-improvements)
   - [Implementation of the colorama Library](#implementation-of-the-colorama-library)
10. [Future Improvements](#future-improvements)
   - [Google Maps JavaScript API](#google-maps-javascript-api)
   - [Dynamic Data loading](#dynamic-data-loading)
   - [Filtering and Sorting](#filtering-and-sorting)
11. [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
12. [Deployment](#deployment)
    - [Cloning & Forking](#cloning--forking)
    - [Local Deployment](#local-deployment)
    - [Remote Deployment (Heroku)](#remote-deployment-heroku)
13. [Credits](#credits)
    - [Source Code](#source-code)
    - [Useful links](#useful-links)
    - [Tools](#tools)
    - [Resources](#resources)
14. [License](#license)

## Technologies Used

- [Django](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/)
- [Bootstrap](https://getbootstrap.com/)
- [jQuery](https://jquery.com/)
- [FullCalendar](https://fullcalendar.io/)
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview)
- [Font Awesome](https://fontawesome.com/)
- [Ajax](https://api.jquery.com/jquery.ajax/)
- [Tippy.js](https://atomiks.github.io/tippyjs/)
- [Moment.js](https://momentjs.com/)
- [Heroku](https://www.heroku.com/)
- [SendGrid](https://sendgrid.com/)


### Django
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It is used to build the server-side functionality of the Social Event Planner, including handling HTTP requests, database operations, and user authentication.

   ```python
   from django.shortcuts import render, redirect
   from django.contrib.auth.decorators import login_required
   from .models import Event

   @login_required
   def dashboard(request):
      events = Event.objects.filter(user=request.user)
      return render(request, "dashboard.html", {"events": events})
   ```

### SQLite
Django's built-in SQLite is used as the database for this project. It is a lightweight, disk-based database that doesn’t require a separate server process, making it easy to set up and use.

   ```python
   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
      }
   }
   ```

### Bootstrap
Bootstrap is a front-end framework for developing responsive and mobile-first websites. It provides CSS and JavaScript-based design templates for typography, forms, buttons, navigation, and other interface components.

   ```html
   <div class="container">
      <h1 class="mt-4">Event Dashboard</h1>
      <button class="btn btn-primary">Add Event</button>
   </div>
```

### jQuery
jQuery is a fast, small, and feature-rich JavaScript library. It simplifies things like HTML document traversal and manipulation, event handling, and animation, making it easier to develop dynamic and interactive web pages.

   ```javascript
   <script>
   $(document).ready(function(){
      $("#addEventBtn").click(function(){
         $("#eventModal").modal('show');
      });
   });
   </script>
   ```

### FullCalendar
FullCalendar is a JavaScript calendar library for creating interactive and customizable calendars. It is used to display events in a calendar view, allowing users to see their schedules at a glance.

   ```html
   <div id='calendar'></div>
   <script>
      $(document).ready(function() {
         $('#calendar').fullCalendar({
               events: '/api/events/', // URL to fetch events
         });
      });
   </script>
   ```

### Google Places API
The Google Places API is a service that returns information about places using HTTP requests. It is used to enhance event location input by providing autocomplete functionality and additional place details.

   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"></script>
   <input id="location" type="text" placeholder="Enter a location">
   <script>
      var input = document.getElementById('location');
      var autocomplete = new google.maps.places.Autocomplete(input);
   </script>
   ```

### Font Awesome
Font Awesome is a font and icon toolkit based on CSS and LESS. It is used to add scalable vector icons that can be customized with CSS.
   
   ```html
   <i class="fas fa-calendar-alt"></i> Calendar
   ```

### Ajax
Ajax is used to perform asynchronous HTTP requests to update parts of a web page without reloading the whole page. It enhances the user experience by providing faster and more dynamic interactions.

   ```javascript
   $.ajax({
      url: '/api/events/',
      method: 'GET',
      success: function(data) {
         $('#eventsList').html(data);
      }
   });
   ```

### Tippy.js
Tippy.js is a lightweight, highly customizable tooltip and popover library. It is used to display additional information about events when users hover over them in the calendar.
   
   ```javascript
   <button data-tippy-content="Event details">Event Info</button>
   <script>
      tippy('[data-tippy-content]');
   </script>
   ```

### Moment.js
Moment.js is a JavaScript library for parsing, validating, manipulating, and displaying dates and times. It is used in conjunction with FullCalendar to handle date and time formatting.

   ```javascript
   var date = moment().format('MMMM Do YYYY, h:mm:ss a')
   ```
### Heroku
Heroku is a cloud platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud. It is used to deploy and host the Social Event Planner web application.

   ```bash
   # Deployment command
   git push heroku main
   ```

### SendGrid
SendGrid is a cloud-based email service that provides reliable email delivery and scalability. It is used to send transactional emails, such as password reset links and event invitations, to users of the Social Event Planner.

   ```python
   from django.core.mail import send_mail

   def send_invitation(email, event):
      send_mail(
         'You are invited!',
         f'Join us at {event.name} on {event.date}.',
         'from@example.com',
         [email],
         fail_silently=False,
      )
   ```  

## User Stories:

### User Story 1: User Authentication
| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to sign up for the event planner platform                                                                                         | I have successfully created an account and logged in     |
| I want to log in to my account                                                                                                           | I can access my dashboard with my user credentials        |
| I want to log out of my account                                                                                                          | I am redirected to the homepage and my session is ended   |

### User Story 2: Event Creation

| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to create a new event                                                                                                             | I have filled in the event details and it appears on my calendar and event list |
| I want to edit an event I created                                                                                                        | I can update the event details and see the changes reflected |
| I want to use Google Places Autocomplete for event location                                                                              | I can easily select a location using autocomplete suggestions |
| I want to delete an event I created                                                                                                      | The event is removed from my event list and calendar     |

### User Story 3: Invitation System
| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to invite friends to my event                                                                                                     | My friends receive an invitation and can RSVP            |
| I want to select friends from a list to send invitations                                                                                 | I can easily choose friends from my friend list to invite |
| I want to accept an event invitation                                                                                                     | My RSVP status is updated to 'Accepted'                  |
| I want to decline an event invitation                                                                                                    | My RSVP status is updated to 'Declined' and the event is grayed out |
| I want to see the status of my event invitations                                                                                         | I can see who has accepted, declined, or not responded to my invitations |
| I want to manage invitations and see who has viewed and responded                                                                        | I can track invitation views and responses in real-time  |


### User Story 4: Availability
| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to see the availability of other users for an event                                                                               | I can view the availability of invited users for an event |
| I want to suggest alternate dates for events                                                                                             | I can propose new dates for events and see responses     |

### User Story 5: Friendship System
| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to search for friends on the platform                                                                                             | I can find and send friend requests to other users       |
| I want to accept or decline friend requests                                                                                              | I can manage incoming friend requests from other users   |
| I want to see a list of my friends                                                                                                       | All my friends are displayed in a list with their profile pictures |
| I want to view a friend's profile                                                                                                        | I can click on a friend and see their profile details     |
| I want to remove a friend                                                                                                                | The friend is removed from my friend list                 |
| I want to confirm before removing a friend                                                                                               | A confirmation modal appears when I attempt to remove a friend |
| I want to see a list of sent friend requests                                                                                             | I can track all the friend requests I have sent          |
| I want to see a list of received friend requests                                                                                         | I can view and manage all the friend requests I have received |

### User Story 6: Notification System
| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to see notifications of new events or updates                                                                                     | New notifications appear in my notification dropdown     |
| I want to mark a notification as read                                                                                                    | The notification is marked as read and the unread count decreases |
| I want to see all my notifications                                                                                                      | I can view a list of all my past notifications            |
| I want to receive real-time updates for new notifications                                                                                | I get alerts and the notification count updates without refreshing the page |


### User Story 7: Dashboard
| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to see a list of my upcoming events                                                                                                | All my future events are displayed in the upcoming events list |
| I want to see a list of events I have created                                                                                            | All events I have created are displayed in a separate list |
| I want to view past events                                                                                                               | Past events are visible on my calendar                    |
| I want to see a calendar view of all events                                                                                              | All events I am invited to or have created are displayed on the calendar |
| I want to see tooltips with event details when hovering over calendar events                                                             | Tooltips appear with event details when I hover over events on the calendar |
| I want to see a loading spinner while event details tooltip loads                                                                        | A spinner is displayed while event details are being loaded |
| I want to view the details of an event                                                                                                   | I can click on an event and see all its details          |
| I want to see color-coded event statuses                                                                                                 | Different event statuses are displayed in various colors for easy identification |
| I want to edit and delete events I have created                                                                                         | I can modify or remove my events directly from the dashboard |
| I want to confirm before deleting an event                                                                                              | A confirmation modal appears when I attempt to delete an event |


### User Story 8: Profile Management
| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to manage my profile information                                                                                                  | I can update my profile details and profile picture      |
| I want to change my password                                                                                                             | I can update my password and log in with the new credentials |
| I want to reset my password if I forget it                                                                                               | I can request a password reset via email  
| I want to delete my account                                                                                                              | My account is permanently deleted and all data is removed |
| I want to confirm before deleting my account                                                                                             | A confirmation modal appears when I attempt to delete my account |


## Wireframes:

#### Site Map
- The site map visually outlines the structure of the website, showing the relationships between different pages and sections. It provides an overview of how users will navigate through the platform, ensuring an intuitive user experience.
![site map](README/images/site-map.png)

#### Database Schema
- The database schema diagram illustrates the data model used in the application. It includes the tables, their relationships, and key fields, ensuring data integrity and efficient data management.
![data base schema](README/images/database-model.png)

#### color palette
- The color palette is used to define the primary and secondary colors of the application. It helps maintain a consistent visual style and branding throughout the platform.
![color palette](README/images/color-palette.png)
   - Coolors.co was used to generate the color palette for the application.

## Features
- The Social Event Planner application provides a range of features to help users create, manage, and share events with their friends. The features are designed to enhance user experience, improve productivity, and facilitate social interactions.

#### User Authentication
- Sign Up: Users can create a new account using their email address and a password.
   ![signup](README/images/feat-signup.png)
- Login: Registered users can log in using their email and password.
   ![login](README/images/feat-login.png)
- Logout: Users can securely log out of their accounts.
   ![logout](README/images/feat-logout.png)
- Password Reset: Users can reset their password via email if they forget it.
   ![password reset](README/images/feat-forgot-password.png)
- Account Management: Users can update their profile information, including changing their password.
   ![profile](README/images/feat-profile.png)
   ![profile picture](README/images/feat-profile-pic.png)
   ![profile delete](README/images/feat-profile-delete.png)

#### Event Creation and Management
- Create Event: Users can create new events by providing details such as title, date, time, location, and description.
   ![create event](README/images/feat-add-event.png)
- Edit Event: Users can edit the details of their events.
   ![edit event](README/images/feat-event-edit.png)
- Delete Event: Users can delete their events, which will also delete all associated invitations and responses.
   ![delete event](README/images/feat-dashboard-delete.png)
- View Event Details: Users can view detailed information about an event, including the list of invited participants and their responses, and suggested dates/times.
   ![event details](README/images/feat-event-details.png)

#### Invitation System
- Send Invitations: Event creators can invite friends to their events.
   ![send invitations](README/images/feat-invitations-add.png)
- Manage Invitations: Users can view and manage invitations they have sent or received.
   ![manage invitations](README/images/feat-invitations-manage-full.png)
- Respond to Invitations: Invited users can accept, decline, or mark their response as "maybe".
   ![respond invitations](README/images/feat-response.png)
- Suggestions: Users can suggest alternate dates for events and see responses from other participants.
   ![suggestions](README/images/feat-suggest.png)

#### Notification System
- Real-Time Notifications: Users receive notifications for event updates, invitations, and responses.
   ![notifications](README/images/feat-notifications-dropdown.png)
- Read/Unread Status: Notifications can be marked as read or unread.
- Notification Center: A dropdown menu shows the most recent notifications with links to relevant actions.
   ![notifications](README/images/feat-notifications-page.png)

#### Friend Management
- Add Friends: Users can send friend requests to other users.
- Manage Friend Requests: Users can view and respond to incoming friend requests.
- View Friends: Users can view a list of their friends and access their profiles.
   ![friends list](README/images/feat-friends-page.png)
- Remove Friends: Users can unfriend someone from their friend list.
   ![remove friend](README/images/feat-friends-delete.png)

#### Calendar Integration
- Interactive Calendar: Events are displayed in a calendar view, allowing users to see their schedule at a glance.
- Color-Coded Events: Events are color-coded based on their status (confirmed, pending, cancelled).
   ![calendar](README/images/dashboard.png)
- Event Status Indicators: Additional indicators for user responses (accepted, declined, maybe).
   ![event status](README/images/feat-filter.gif)
- Event Tooltips: Hovering over an event shows a tooltip with detailed information about the event.
   ![event tooltip](README/images/feat-tooltip.gif)

#### Location Services
- Google Places Autocomplete: Integrated autocomplete for event location input, enhancing user experience and accuracy.
   ![location autocomplete](README/images/feat-autocomplete.gif)

#### User Dashboard
- Upcoming Events: A list of upcoming events that the user is either hosting or invited to.
- Your Events: A separate list showing events created by the user.
   ![dashboard](README/images/dashboard.png)
- Event Management Tools: Quick access to edit or delete events from the dashboard.
   ![dashboard](README/images/feat-dashboard-delete.png)

#### Dynamic Data Integration
- Real-Time Data Updates: Notifications are dynamically updated without requiring a page refresh.
- Ajax Integration: Used for updating the notification count and notification dropdown without reloading the page.
   ![notifications](README/images/feat-notifications-dropdown.png)

#### Error Handling
- User-Friendly Error Messages: Clear and concise error messages are displayed for validation errors and other issues.
- Fallback Mechanisms: Ensures the application continues to function smoothly in case of minor issues.
   ![error message](README/images/feat-error-message.png)

#### Responsive Design
- Mobile-Friendly: The application is designed to be fully responsive and works well on mobile devices.
- Adaptive UI Elements: Elements such as dropdowns, modals, and forms adapt to different screen sizes for an optimal user experience.
   ![responsive](README/images/responsive-dropdown.png)

#### Security Features
- CSRF Protection: Cross-Site Request Forgery protection is enabled to secure forms.
   ```html
   <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Sign Up</button>
   </form>
   ```
   - the {% csrf_token %} template tag generates a CSRF token that Django checks when the form is submitted.

- Password Hashing: User passwords are securely hashed using Django’s built-in mechanisms.
   
   ```python
   def set_new_password(request):
    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if new_password == confirm_password:
            request.user.set_password(new_password)  # Hashes the password
            request.user.save()
            return redirect("account_login")
   ```
   - The set_password method hashes the password before saving it to the database, ensuring that plain-text passwords are never stored.
   - The request.user.set_password(new_password) hashes the new password using Django's default hashing algorithm before saving it to the database.

- SSL/TLS: Ensures data is encrypted during transmission.
   ```python
   SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
   SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
   CSRF_COOKIE_SECURE = True     # Ensure the CSRF cookie is only sent over HTTPS
   ```

- Cache Control: Prevent caching of sensitive pages.
   ```python
   @login_required
   @cache_control(no_cache=True, must_revalidate=True, no_store=True)
   def dashboard(request):
      ...
   ```

- Additional Security Features
   ```python
   @login_required
   def profile(request):
      ...
   ```
   - the @login_required decorator to ensure that certain views are only accessible to authenticated users.

#### Additional Features
- Progress Indicators: Loading spinners provide feedback during data fetching and processing.
   ![loading spinner](README/images/feat-tooltip.gif)
- Reporting: Detailed reports on event participation and user activity.
   ![reports](README/images/feat-response.png)

## MoSCoW Prioritization
- The MoSCoW method is used to prioritize features based on their importance and urgency. Features are categorized into Must Have, Should Have, Could Have, and Won't Have for the current version of the application.

### Must Have

| Feature                          | Description                                                                                       |
|----------------------------------|---------------------------------------------------------------------------------------------------|
| User Authentication              | Users must be able to sign up, log in, and log out. Unique usernames and emails are required.     |
| Event Creation                   | Users must create new events with title, description, date, and location (Google Places API).     |
| Invitation System                | Users must invite friends to events and see invitation status. Friends must RSVP.                |
| Dashboard                        | Users must see upcoming, past events, calendar view, edit/delete events, color-coded status, and modals for deletion/alternate dates.  |
| Friendship System                | Users must search for friends, send friend requests, view friends’ profiles, and remove friends. Friends’ profile pictures must be shown. |
| Notification System              | Users must receive notifications for events, updates, and friend requests. Notifications must update in real-time with alerts. |
| Availability                     | Users must see friend availability for events and suggest alternate dates.                      |

### Should Have

| Feature                          | Description                                                                                       |
|----------------------------------|---------------------------------------------------------------------------------------------------|
| User Profile Management          | Users should update profile information, profile picture, change password, and reset password.    |
| Event Management                 | Users should suggest alternate event dates and see responses.                                     |
| Home Page                        | Should introduce the event planner platform and provide a call to action.                         |
| Error Handling                    | Users should see clear error messages for validation errors and other issues.                     |

### Could Have

| Feature                          | Description                                                                                       |
|----------------------------------|---------------------------------------------------------------------------------------------------|
| Advanced Search and Filtering    | Users could filter events by type, location, date range, and search by keyword.                   |
| Enhanced Notifications           | Users could receive email notifications and customize settings.                                   |
| Analytics and Reporting          | Users could view analytics on event participation and friend interactions.                        |

### Won't Have (for now)

| Feature                          | Description                                                                                       |
|----------------------------------|---------------------------------------------------------------------------------------------------|
| Integration with Social Media    | Integration for event sharing and friend invitations on social media platforms.                   |
| Monetization Features            | Features like paid events, ticketing, or advertisements.                                          |
| Gamification                     | Points, badges, or rewards for event participation and friend interactions.                       |
| Password Reset | Users can reset their password via email if they forget it. |

## GitHub Projects, Milestones, and Issues

### GitHub Projects
GitHub Projects was used to manage and organize tasks. It provides a Kanban-style board that allows to visualize our workflow and track the progress of tasks.

### Milestones
Milestones are used to track the progress of significant phases in our project. Each milestone includes a set of issues that need to be completed to achieve the milestone goal.

### Issues
Issues are used to track tasks, enhancements, and bugs for the project. Each issue is assigned to a team member and linked to a milestone.

For more details, visit the [GitHub Project](https://github.com/users/jeffdruid/projects/3) page.


## Troubleshooting
- Password Reset: Users can reset their password via email if they forget it.
   - ~~The password reset functionality is implemented using Django's built-in password reset views and templates. Users can request a password reset by entering their email address, and an email with a reset link will be sent to them. The link contains a unique token that allows users to set a new password. The password reset link is valid for a limited time and can only be used once.~~
   ![password reset](README/images/feat-reset-disabled.png)
   - This feature was replaced with an one time link sent to the user's email to reset their password.
   ![password reset](README/images/feat-forgot-password.png)
   ![password reset email](README/images/feat-email-reset.png)
   ![password reset form](README/images/feat-set-password.png)

## Testing
All testing was done manually and automated using Django's built-in testing framework. The application was tested for functionality, user experience, and security. Test cases were created to cover user stories and edge cases, ensuring the application works as expected.
   - You can view all the tests [here](README/TESTING.md)

## Bugs
### Bug Report: send_one_time_login_link_form Functionality
The send_one_time_login_link_form function is responsible for handling requests to generate a one-time login link for users who have requested a password reset. 
- This function processes form submissions containing an email address and redirects users to generate and send the login link.

   ```python
   def send_one_time_login_link_form(request):
      if request.method == "POST":
         email = request.POST.get("email")
         return redirect("send_one_time_login_link", user_email=email)
      return render(request, "accounts/send_one_time_login_link_form.html")
   ```

   - However, several issues in this code can lead to potential security vulnerabilities and functional problems.
   - The function send_one_time_login_link_form requires enhancements in terms of input validation, security, and user feedback to ensure robust functionality and protection against common vulnerabilities. 
   - **This feature is disabled in the current version of the application to prevent potential security risks.**

   - commit: [send_one_time_login_link_form](https://github.com/jeffdruid/planpal/commit/5c8351adcece1721891f421d876733fb72c7a64f)

### Fixed Bugs
### Bug: Profile Picture Modal Not Closing

- The profile picture modal was not closing when clicking outside the modal or on the "X" button.

   ```javascript
   <!-- JavaScript for closing modals -->
   <script>
      window.onclick = function(event) {
         const profilePictureModal = $('#profilePictureModal');
         if (event.target == profilePictureModal[0]) {
               closeProfilePictureModal();
         }
      }
   </script>
   ```
   - Ensure the correct Bootstrap modal methods are called and fix the JavaScript code to handle the closing functionality properly.

   ```javascript
   <!-- JavaScript for closing modals -->
   <script>
      $(document).ready(function() {
         // Close the profile picture modal when clicking outside
         $(window).on('click', function(event) {
               if ($(event.target).is('#profilePictureModal')) {
                  $('#profilePictureModal').modal('hide');
               }
         });

         // Ensure modals close on clicking 'X'
         $('.modal .close').on('click', function() {
               $(this).closest('.modal').modal('hide');
         });
      });
   </script>
   ```
   
   - The updated JavaScript code ensures that the profile picture modal closes when clicking outside the modal or on the "X" button.
   - The modal is hidden using the Bootstrap modal('hide') method to ensure proper functionality.
   - The modal close functionality is now working as expected, allowing users to close the modal by clicking outside or on the "X" button.

## UI Improvements
- The user interface was improved to enhance the user experience and make the application more visually appealing.
- Bootstrap 5 was used to create a responsive and modern design for the application.

## Future Improvements

#### Google Maps JavaScript API
- The Google Maps JavaScript API would be used to embed maps into the web pages and provide location-based services, such as displaying event locations on a map.

#### Dynamic Data Loading
- Real-Time Data Updates: Data on the dashboard, calendar, and event responses could be updated in real-time using WebSockets or other technologies.

#### Filtering and Sorting
- Enhanced Filtering: Users could filter events based on criteria such as date, location, or event type.
- Sorting Options: Additional sorting options could be added to the event list, such as by date, title, or status.

## Setup

### Prerequisites

- Python 3.9 or higher
- Django 4.2.13
- SendGrid account for email services
- Heroku CLI (for deployment)
- Git

### Installation

Clone the repository
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```
On macOS and Linux:
```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set environment variables:

Create a .env file and add the following environment variables:

```
makefile
DEFAULT_FROM_EMAIL_KEY=your_email@example.com
EMAIL_HOST_PASSWORD_KEY=your_sendgrid_api_key
SECRET_KEY=your_secret_key
```

### Usage

Run the development server:

```bash
python manage.py runserver
```

Open your browser and go to http://127.0.0.1:8000/ to access the application.

## Deployment

### Cloning & Forking
Fork the repository on GitHub to your own account.

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/your-forked-repo.git
```

### Local Deployment

Run database migrations:


```bash
python manage.py migrate
```

Create a superuser:


```bash
python manage.py createsuperuser
```

Collect static files:

```bash
python manage.py collectstatic
```

### Remote Deployment (Heroku)

Login to Heroku:

```bash
heroku login
```

Create a new Heroku app:

```bash
heroku create your-app-name
```

Set environment variables on Heroku:

```bash
heroku config:set DEFAULT_FROM_EMAIL_KEY=your_email@example.com
heroku config:set EMAIL_HOST_PASSWORD_KEY=your_sendgrid_api_key
heroku config:set SECRET_KEY=your_secret_key
```

```bash
git push heroku main
```

Run database migrations on Heroku:

```bash
heroku run python manage.py migrate
```

Open your app:

```bash
heroku open
```

## Credits

- [Default Profile Picture SVG](https://en.m.wikipedia.org/wiki/File:Default_pfp.svg)
- [Fix Sendgrid Integration - Change from SMTP to API Key Usage](https://www.youtube.com/watch?v=T3RC7UBAB18)
- [Password Reset Email | Django (3.0) Crash Course Tutorials (pt 20)](https://www.youtube.com/watch?v=sFPcd6myZrY&t=979s)
- [Python Django Tutorial: Full-Featured Web App Part 12 - Email and Password Reset](https://www.youtube.com/watch?v=-tyBEsHSv7w&t=1065s)
- [Coolors - Color Palette Generator](https://coolors.co/)

### Useful Links

- [Python Django Web Framework - Full Course for Beginners](https://www.youtube.com/watch?v=F5mRW0jo-U4&t=302s)
- [Heroku: Reduce Slug Size With .slugignore](https://devcenter.heroku.com/articles/slug-compiler#ignoring-files-with-slugignore)

### Tools
- [Visual Studio Code](https://code.visualstudio.com/)
- [GitHub](https://github.com)
- [Heroku](https://www.heroku.com/)
- [Database Relationship Diagrams Design Tool](https://dbdiagram.io/)
- [Site Map Design Tool - Balsamiq](https://balsamiq.com/)
- [W3C HTML Validator](https://validator.w3.org/)
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [Jshint](https://jshint.com/)
- [Django's Built-in Check System](https://docs.djangoproject.com/en/3.2/ref/django-admin/#check)
- [WAVE - Web Accessibility Evaluation Tool](https://wave.webaim.org/)
- [LightHouse](https://developers.google.com/web/tools/lighthouse)
- [CI Python Linter](https://pep8ci.herokuapp.com/)

### Resources
- [Django Documentation](https://docs.djangoproject.com/en/3.2/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [Sendgrid Documentation](https://sendgrid.com/docs/)
- [MoSCoW Prioritization](https://www.productplan.com/glossary/moscow-prioritization/)
- [GitHub Projects](https://docs.github.com/en/issues/organizing-your-work-with-project-boards/managing-project-boards/about-project-boards)

### License
- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**[Back to top](#table-of-contents)**