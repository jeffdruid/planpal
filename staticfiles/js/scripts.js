// Load the notification dropdown when the bell icon is clicked
$(document).ready(function() {
    $("#notificationBell").click(function(e) {
        e.preventDefault();
        $("#notificationDropdown").toggle();
    });

    $(document).click(function(e) {
        if (!$(e.target).closest('.notification-dropdown, #notificationBell').length) {
            $("#notificationDropdown").hide();
        }
    });

    $("#profileLink").click(function(e) {
        e.preventDefault();
        $("#profileDropdown").toggle();
    });

    $(document).click(function(e) {
        if (!$(e.target).closest('#profileDropdown, #profileLink').length) {
            $("#profileDropdown").hide();
        }
    });
});

function respondToInvitation(response) {
    if (response === 'deny' || response === 'maybe') {
        document.getElementById('alternateDateModal').style.display = 'block';
    } else {
        alert('Invitation accepted!');
    }
}

function closeModal() {
    document.getElementById('alternateDateModal').style.display = 'none';
}

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    if (event.target == document.getElementById('alternateDateModal')) {
        closeModal();
    }
}

// Handle the alternate date form submission
document.getElementById('alternateDateForm').onsubmit = function(event) {
    event.preventDefault();
    let alternateDate = document.getElementById('alternate_date').value;
    alert('Suggested alternate date: ' + alternateDate);
    closeModal();
}
