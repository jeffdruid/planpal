// Load the notification dropdown when the bell icon is clicked
$(document).ready(function() {
    $('#notificationBell').on('click', function() {
        $('#notificationDropdown').toggle();
    });

    // Close the dropdown if clicked outside
    $(document).on('click', function(event) {
        if (!$(event.target).closest('#notificationBell').length) {
            $('#notificationDropdown').hide();
        }
    });
});
