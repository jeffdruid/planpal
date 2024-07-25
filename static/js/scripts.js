function toggleDropdown(elementId) {
    var dropdown = document.getElementById(elementId);
    if (dropdown.style.display === "block") {
        dropdown.style.height = dropdown.scrollHeight + 'px';
        dropdown.style.opacity = 1;
        window.setTimeout(function() {
            dropdown.style.height = '0';
            dropdown.style.opacity = 0;
        }, 10);  // Add a small delay for the height change to take effect
        window.setTimeout(function() {
            dropdown.style.display = 'none';
        }, 300);  // Match this to the duration of your CSS transition
    } else {
        dropdown.style.display = 'block';
        dropdown.style.height = '0';
        dropdown.style.opacity = 0;
        window.setTimeout(function() {
            dropdown.style.height = dropdown.scrollHeight + 'px';
            dropdown.style.opacity = 1;
        }, 10);  // Add a small delay for the height change to take effect
    }
}

function openAlternateDateModal() {
    $('#alternateDateModal').modal('show');
}

let previousUnreadCount = initialUnreadCount;

function fetchNotifications() {
    console.log("Fetching notifications...");
    $.ajax({
        url: '/notifications/get-notifications/',  // Ensure this matches the Django URL pattern
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log("Notifications fetched successfully:", data);
            let currentUnreadCount = data.unread_count;

            if (currentUnreadCount > previousUnreadCount) {
                // alert("You have a new notification!");
                console.log("New notification detected!");
                updateNotifications(data.notifications, currentUnreadCount - previousUnreadCount);
            }

            // Update the unread count badge
            let badge = $("#notificationBell .badge");
            badge.text(currentUnreadCount > 0 ? currentUnreadCount : '');
            if (currentUnreadCount > 0) {
                badge.css('display', 'inline-block');
                badge.css('opacity', 0);
                badge.css('opacity', 1);
                // badge.animate({opacity: 1}, 300);
            } else {
                badge.css('display', 'none');
            }

            previousUnreadCount = currentUnreadCount;
        },
        error: function(xhr, status, error) {
            console.error("Error fetching notifications:", xhr.status, xhr.statusText);
            // console.log("Response:", xhr.responseText);
        }
    });
}

function updateNotifications(notifications, newNotificationCount) {
    console.log("Updating notifications dropdown...");
    let dropdownMenu = $("#notificationDropdown");

    // Remove "No notifications" if present
    dropdownMenu.find('a.dropdown-item:contains("No notifications")').remove();

    // Add new notifications to the dropdown
    notifications.slice(0, newNotificationCount).forEach(function(notification) {
        let notificationUrl;
        if (notification.type === "event") {
            notificationUrl = `/notifications/notifications/mark-read/${notification.id}/`;
        } else if (notification.type === "friend_request_received") {
            notificationUrl = `/notifications/notifications/mark-read/${notification.id}/`;
        } else {
            notificationUrl = `/notifications/notifications/mark-read/${notification.id}/`;
        }

        let notificationItem = `
            <a class="dropdown-item" href="${notificationUrl}">
                ${notification.message}
                <small class="text-muted">${notification.created_at}</small>
            </a>`;
        dropdownMenu.prepend(notificationItem);
    });

    // Ensure "View All Notifications" is always present
    if (!dropdownMenu.find('a[href="/notifications/"]').length) {
        dropdownMenu.append('<div class="dropdown-divider"></div><a class="dropdown-item" href="/notifications/">View All Notifications</a>');
    }

    // Handle display state when there are no notifications
    if (notifications.length === 0) {
        dropdownMenu.append('<a class="dropdown-item" href="#">No notifications</a>');
    }
}

$(document).ready(function() {

    $("#notificationBell").click(function(e) {
        e.preventDefault();
        console.log("Notification bell clicked.");
        toggleDropdown("notificationDropdown");
        document.getElementById("profileDropdown").style.display = 'none'; // Hide profile dropdown when notification dropdown is opened
        fetchNotifications();
    });

    // Toggle profile dropdown
    $("#profileLink").click(function(e) {
        e.preventDefault();
        console.log("Profile link clicked.");
        toggleDropdown("profileDropdown");
        document.getElementById("notificationDropdown").style.display = 'none'; // Hide notification dropdown when profile dropdown is opened
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
            contentHeight: 900,
            events: window.calendarEvents, // Load events from a global variable
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

                // Simulate a delay for loading content
                setTimeout(function() {
                    $('.fc-tooltip').html(
                        '<strong>' + event.title + '</strong><br>' +
                        'Date: ' + moment(event.start).format('MMMM Do YYYY') + '<br>' +
                        'Time: ' + moment(event.start).format('h:mm a') + '<br>' +
                        'Location: ' + event.location + '<br>' +
                        'Description: ' + event.description + '<br>' +
                        'Created by: ' + event.creator
                    );
                }, 1000);  // Adjust the delay as needed
            },
            eventMouseout: function(event, jsEvent) {
                $('.fc-tooltip').remove();
            }
        });
    }

    // https://stackoverflow.com/questions/47710304/how-to-change-row-height-in-fullcalendar
    
    // Modify contentHeight based on window size
    function adjustCalendarContentHeight() {
        var contentHeight = $(window).width() < 992 ? 400 : 900;
        $('#calendar').fullCalendar('option', 'contentHeight', contentHeight);
    }

    adjustCalendarContentHeight(); // Adjust on document ready

    $(window).resize(function() {
        adjustCalendarContentHeight(); // Adjust on window resize
    });

    // Event delete modal functionality
    var deleteModal = $('#deleteModal');
    var deleteForm = $('#deleteForm');

    $('.delete-btn').click(function() {
        var eventId = $(this).data('event-id');
        deleteForm.attr('action', '/events/' + eventId + '/delete/');
        deleteModal.modal('show');
    });

    $('#deleteModal .close, #deleteModal button[data-dismiss="modal"]').click(function() {
        deleteModal.modal('hide');
    });

    // Delete friend modal functionality
    var deleteFriendModal = $('#deleteFriendModal');
    var deleteFriendForm = $('#deleteFriendForm');

    $('.delete-friend-btn').click(function() {
        var friendId = $(this).data('friend-id');
        deleteFriendForm.attr('action', '/delete_friend/' + friendId + '/');
        deleteFriendModal.modal('show');
    });

    $('#deleteFriendModal .close, #deleteFriendModal button[data-dismiss="modal"]').click(function() {
        deleteFriendModal.modal('hide');
    });

    // Close modals when clicking outside
    window.onclick = function(event) {
        if (event.target == deleteModal[0]) {
            deleteModal.modal('hide');
        }
        if (event.target == deleteFriendModal[0]) {
            deleteFriendModal.modal('hide');
        }
        if (event.target == $('#alternateDateModal')[0]) {
            $('#alternateDateModal').modal('hide');
        }
    };

    // Function to close all modals
    function closeModal() {
        $('#deleteFriendModal').modal('hide');
        $('#deleteModal').modal('hide');
        $('#alternateDateModal').modal('hide');
    }

    // Alternate date form submission
    $('#alternateDateForm').on('submit', function(event) {
        event.preventDefault();
        $(this).unbind('submit').submit();
    });

    // Fetch notifications every 10 seconds if user is authenticated
    if (userIsAuthenticated) {
        console.log("User is authenticated.");
        setInterval(fetchNotifications, 10000);
    } else {
        console.log("User is not authenticated.");
    }
        
});
