function openAlternateDateModal() {
    $('#alternateDateModal').modal('show');
}

$(document).ready(function() {
    // Toggle notification dropdown
    $("#notificationBell").click(function(e) {
        e.preventDefault();
        $("#notificationDropdown").toggle();
        $("#profileDropdown").hide(); // Hide profile dropdown when notification dropdown is opened
    });

    // Toggle profile dropdown
    $("#profileLink").click(function(e) {
        e.preventDefault();
        $("#profileDropdown").toggle();
        $("#notificationDropdown").hide(); // Hide notification dropdown when profile dropdown is opened
    });

    // Close dropdowns when clicking outside
    $(document).click(function(e) {
        if (!$(e.target).closest('.dropdown-menu, #notificationBell, #profileLink').length) {
            $(".dropdown-menu").hide();
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
            events: window.calendarEvents, // Load events from a global variable
            timeFormat: 'h:mma',
            eventMouseover: function(event, jsEvent) {
                var tooltip = '<div class="fc-tooltip">' +
                                '<strong>' + event.title + '</strong><br>' +
                                'Date: ' + moment(event.start).format('MMMM Do YYYY') + '<br>' +
                                'Time: ' + moment(event.start).format('h:mm a') + '<br>' +
                                'Location: ' + event.location + '<br>' +
                                'Description: ' + event.description + 
                                'Created by: ' + event.creator +
                              '</div>';
                $("body").append(tooltip);
                $(this).mouseover(function(e) {
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
                });
            },
            eventMouseout: function(event, jsEvent) {
                $('.fc-tooltip').remove();
            }
        });
    }

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
});
