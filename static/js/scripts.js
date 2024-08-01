/**
 * Dropdown Toggle Functions
 */

// Function to toggle dropdown display with smooth transition
function toggleDropdown(elementId) {
    var dropdown = document.getElementById(elementId);
    if (dropdown.style.display === "block") {
        dropdown.style.height = dropdown.scrollHeight + 'px';
        dropdown.style.opacity = 1;
        window.setTimeout(function() {
            dropdown.style.height = '0';
            dropdown.style.opacity = 0;
        }, 10);
        window.setTimeout(function() {
            dropdown.style.display = 'none';
        }, 300);
    } else {
        dropdown.style.display = 'block';
        dropdown.style.height = '0';
        dropdown.style.opacity = 0;
        window.setTimeout(function() {
            dropdown.style.height = dropdown.scrollHeight + 'px';
            dropdown.style.opacity = 1;
        }, 10);
    }
}

/**
 * Notifications Functions
 */

let previousUnreadCount = initialUnreadCount;

// Function to fetch notifications from the server
function fetchNotifications() {
    $.ajax({
        url: '/notifications/get-notifications/',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            let currentUnreadCount = data.unread_count;

            if (currentUnreadCount > previousUnreadCount) {
                updateNotifications(data.notifications);
            }

            let badge = $("#notificationBell .badge");
            badge.text(currentUnreadCount > 0 ? currentUnreadCount : '');
            if (currentUnreadCount > 0) {
                badge.css('display', 'inline-block');
                badge.css('opacity', 1);
            } else {
                badge.css('opacity', 0);
            }

            previousUnreadCount = currentUnreadCount;
        },
        error: function(xhr, status, error) {
            console.error("Error fetching notifications:", xhr.status, xhr.statusText);
        }
    });
}

// Function to update the notifications dropdown menu
function updateNotifications(notifications) {
    let dropdownMenu = $("#notificationDropdown");

    // Clear existing notifications
    dropdownMenu.empty();

    notifications.forEach(function(notification) {
        let notificationUrl = `/notifications/notifications/mark-read/${notification.id}/`;

        let notificationItem = `
            <a class="dropdown-item" href="${notificationUrl}" data-notification-id="${notification.id}">
                ${notification.message}
                <small class="text-muted">${moment(notification.created_at).format("MMMM D, YYYY, h:mm a")}</small>
            </a>`;
        dropdownMenu.prepend(notificationItem);
    });

    // Ensure "View All Notifications" link is present
    if (!dropdownMenu.find('a[href="/notifications/"]').length) {
        dropdownMenu.append('<div class="dropdown-divider"></div><a class="dropdown-item" href="/notifications/">View All Notifications</a>');
    }

    // Handle the display state when there are no notifications
    if (notifications.length === 0) {
        dropdownMenu.append('<a class="dropdown-item" href="#">No notifications</a>');
    }
}

/**
 * FullCalendar Setup and Adjustments
 */

$(document).ready(function() {

    // Notification bell click handler
    $("#notificationBell").click(function(e) {
        e.preventDefault();
        toggleDropdown("notificationDropdown");
        document.getElementById("profileDropdown").style.display = 'none';
        fetchNotifications();
    });

    // Profile link click handler
    $("#profileLink").click(function(e) {
        e.preventDefault();
        toggleDropdown("profileDropdown");
        document.getElementById("notificationDropdown").style.display = 'none';
    });

    // Close dropdowns when clicking outside
    $(document).click(function(e) {
        if (!$(e.target).closest('.dropdown-menu, #notificationBell, #profileLink').length) {
            $(".dropdown-menu").each(function() {
                if ($(this).css("display") == "block") {
                    $(this).css("height", "0");
                    $(this).css("opacity", "0");
                    setTimeout(() => $(this).css("display", "none"), 300);
                }
            });
        }
    });

    // FullCalendar setup
    if ($('#calendar').length) {
        $('#calendar').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            editable: false,
            timeZone: 'local',
            height: 'auto',
            contentHeight: 600,
            events: window.calendarEvents,
            timeFormat: 'h:mma',
            eventMouseover: function(event, jsEvent) {
                var tooltip = '<div class="fc-tooltip">' +
                                '<div class="spinner"></div>' +
                              '</div>';
                $("body").append(tooltip);
                $('.fc-tooltip').css({
                    top: jsEvent.pageY + 10,
                    left: jsEvent.pageX + 20,
                    position: 'absolute',
                    zIndex: 10001,
                    background: '#fff',
                    padding: '10px',
                    border: '1px solid #ccc',
                    borderRadius: '3px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
                }).fadeIn('500').fadeTo('10', 1.9);

                setTimeout(function() {
                    $('.fc-tooltip').html(
                        '<strong>' + event.title + '</strong><br>' +
                        'Date: ' + moment(event.start).format('MMMM Do YYYY') + '<br>' +
                        'Time: ' + moment(event.start).format('h:mm a') + '<br>' +
                        'Location: ' + event.location + '<br>' +
                        'Description: ' + event.description + '<br>' +
                        'Created by: ' + event.creator
                    );
                }, 1000);
            },
            eventMouseout: function(event, jsEvent) {
                $('.fc-tooltip').remove();
            }
        });
    }

    // Function to adjust calendar content height based on window size
    function adjustCalendarContentHeight() {
        var contentHeight = $(window).width() < 992 ? 400 : 600;
        $('#calendar').fullCalendar('option', 'contentHeight', contentHeight);
    }

    adjustCalendarContentHeight();

    $(window).resize(function() {
        adjustCalendarContentHeight();
    });

    // Fetch notifications periodically if user is authenticated
    if (userIsAuthenticated) {
        setInterval(fetchNotifications, 10000);
    } else {
    }
});
