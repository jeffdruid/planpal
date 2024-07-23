# [PlanPal - Social Event Planner](https://planpal-1fe5e3919654.herokuapp.com/)
<a href="https://planpal-1fe5e3919654.herokuapp.com/">
  <img src="planpal banner.png" alt="PlanPal banner" width="100%">
</a>


### Introduction

- Social Event Planner is a web application designed to help users create, manage, and share events with their friends. It provides features for event creation, invitations, notifications, and user profile management.

View the live project [here](https://planpal-1fe5e3919654.herokuapp.com/)

## Table of Contents
TODO - Update table of contents
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
3. [User Stories](#user-stories)
4. [Wireframes](#wireframes)
   - [Site Map](#site-map)
   - [Database Schema](#database-schema)
5. [Features](#features)
   - [Scraping and Validation](#scraping-and-validation)
6. [Troubleshooting](#troubleshooting)
   - [Handling Redirects](#handling-redirects)
7. [Testing](#testing)
   - [Validator Testing](#validator-testing)
     - [flake8](#flake8)
     - [CI Python Linter](#ci-python-linter)
   - [Manual Testing](#manual-testing)
8. [Bugs](#bugs)
   - [Google Sheets Not Opening in a New Tab (Deployment Issue)](#google-sheets-not-opening-in-a-new-tab-deployment-issue)
   - [Fixed Bugs](#fixed-bugs)
     - [Trail slash in the URL](#trail-slash-in-the-url)
9. [UI Improvements](#ui-improvements)
   - [Implementation of the colorama Library](#implementation-of-the-colorama-library)
10. [Future Improvements](#futures-improvements)
   - [Google Maps JavaScript API](#google-maps-javascript-api)
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
    - [Images](#images)
    - [Useful links](#useful-links)
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


### Django
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It is used to build the server-side functionality of the Social Event Planner, including handling HTTP requests, database operations, and user authentication.

### SQLite
Django's built-in SQLite is used as the database for this project. It is a lightweight, disk-based database that doesn’t require a separate server process, making it easy to set up and use.

### Bootstrap
Bootstrap is a front-end framework for developing responsive and mobile-first websites. It provides CSS and JavaScript-based design templates for typography, forms, buttons, navigation, and other interface components.

### jQuery
jQuery is a fast, small, and feature-rich JavaScript library. It simplifies things like HTML document traversal and manipulation, event handling, and animation, making it easier to develop dynamic and interactive web pages.

### FullCalendar
FullCalendar is a JavaScript calendar library for creating interactive and customizable calendars. It is used to display events in a calendar view, allowing users to see their schedules at a glance.

### Google Places API
The Google Places API is a service that returns information about places using HTTP requests. It is used to enhance event location input by providing autocomplete functionality and additional place details.

### Font Awesome
Font Awesome is a font and icon toolkit based on CSS and LESS. It is used to add scalable vector icons that can be customized with CSS.

### Ajax
Ajax is used to perform asynchronous HTTP requests to update parts of a web page without reloading the whole page. It enhances the user experience by providing faster and more dynamic interactions.

### Tippy.js
Tippy.js is a lightweight, highly customizable tooltip and popover library. It is used to display additional information about events when users hover over them in the calendar.

### Moment.js
Moment.js is a JavaScript library for parsing, validating, manipulating, and displaying dates and times. It is used in conjunction with FullCalendar to handle date and time formatting.

### User Stories:

<!-- TODO - Create table of user stories -->

User Story 1: User Authentication

User Story 2: Event Creation

User Story 3: Invitation System

User Story 4: Availability Polling

User Story 5: Consensus Building

User Story 6: Notification System

User Story 7: Dashboard

### Wireframes:

#### Site Map

![site map](site-map.png)

#### database schema

![data base schema](<database model.png>)

### Features
TODO - Add features screenshots

#### User Authentication
- Sign Up: Users can create a new account using their email address and a password.
- Login: Registered users can log in using their email and password.
- Logout: Users can securely log out of their accounts.
<!-- TODO -->
- Password Reset: Users can reset their password via email if they forget it.
<!-- TODO -->
- Account Management: Users can update their profile information, including changing their password.

#### Event Creation and Management
- Create Event: Users can create new events by providing details such as title, date, time, location, and description.
- Edit Event: Users can edit the details of their events.
- Delete Event: Users can delete their events, which will also delete all associated invitations and responses.
- View Event Details: Users can view detailed information about an event, including the list of invited participants and their responses, and suggested dates/times.

#### Invitation System
- Send Invitations: Event creators can invite friends to their events.
- Manage Invitations: Users can view and manage invitations they have sent or received.
- Respond to Invitations: Invited users can accept, decline, or mark their response as "maybe".

#### Notification System
- Real-Time Notifications: Users receive notifications for event updates, invitations, and responses.
- Read/Unread Status: Notifications can be marked as read or unread.
- Notification Center: A dropdown menu shows the most recent notifications with links to relevant actions.

#### Friend Management
- Add Friends: Users can send friend requests to other users.
- Manage Friend Requests: Users can view and respond to incoming friend requests.
- View Friends: Users can view a list of their friends and access their profiles.
- Remove Friends: Users can unfriend someone from their friend list.

#### Calendar Integration
- Interactive Calendar: Events are displayed in a calendar view, allowing users to see their schedule at a glance.
- Event Tooltips: Hovering over an event shows a tooltip with detailed information about the event.
- Color-Coded Events: Events are color-coded based on their status (confirmed, pending, cancelled).
- Event Status Indicators: Additional indicators for user responses (accepted, declined, maybe).

#### Location Services
- Google Places Autocomplete: Integrated autocomplete for event location input, enhancing user experience and accuracy.

#### User Dashboard
- Upcoming Events: A list of upcoming events that the user is either hosting or invited to.
- Your Events: A separate list showing events created by the user.
- Event Management Tools: Quick access to edit or delete events from the dashboard.

#### Dynamic Data Integration
- Real-Time Data Updates: Notifications are dynamically updated without requiring a page refresh.
- Ajax Integration: Used for updating the notification count and notification dropdown without reloading the page.

#### Error Handling
<!-- TODO - Improve error handling -->
- User-Friendly Error Messages: Clear and concise error messages are displayed for validation errors and other issues.
- Fallback Mechanisms: Ensures the application continues to function smoothly in case of minor issues.

#### Responsive Design
- Mobile-Friendly: The application is designed to be fully responsive and works well on mobile devices.
- Adaptive UI Elements: Elements such as dropdowns, modals, and forms adapt to different screen sizes for an optimal user experience.

#### Security Features
- CSRF Protection: Cross-Site Request Forgery protection is enabled to secure forms.
- Password Hashing: User passwords are securely hashed using Django’s built-in mechanisms.
SSL/TLS: Ensures data is encrypted during transmission.

#### Additional Features
- Progress Indicators: Loading spinners provide feedback during data fetching and processing.
- Reporting: Detailed reports on event participation and user activity.


### Future Improvements
#### Google Maps JavaScript API
- The Google Maps JavaScript API would be used to embed maps into the web pages and provide location-based services, such as displaying event locations on a map.

#### Dynamic Data Integration
- Real-Time Data Updates: Data on the dashboard, calendar, and event responses could be updated in real-time using WebSockets or other technologies.

#### Filtering and Sorting
- Enhanced Filtering: Users could filter events based on criteria such as date, location, or event type.
- Sorting Options: Additional sorting options could be added to the event list, such as by date, title, or status.

### Credits

- [Database Relationship Diagrams Design Tool](https://dbdiagram.io/)

### Useful Links

- [Python Django Web Framework - Full Course for Beginners](https://www.youtube.com/watch?v=F5mRW0jo-U4&t=302s)
