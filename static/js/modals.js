$(document).ready(function() {
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
