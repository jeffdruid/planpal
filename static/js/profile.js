function togglePasswordVisibility() {
    const passwordInput = document.getElementById("password");
    const passwordToggle = document.getElementById("passwordToggle");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        passwordToggle.classList.remove("fa-eye");
        passwordToggle.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        passwordToggle.classList.remove("fa-eye-slash");
        passwordToggle.classList.add("fa-eye");
    }
}

function toggleConfirmPasswordVisibility() {
    const confirmPasswordInput = document.getElementById("confirm_password");
    const confirmPasswordToggle = document.getElementById("confirmPasswordToggle");
    if (confirmPasswordInput.type === "password") {
        confirmPasswordInput.type = "text";
        confirmPasswordToggle.classList.remove("fa-eye");
        confirmPasswordToggle.classList.add("fa-eye-slash");
    } else {
        confirmPasswordInput.type = "password";
        confirmPasswordToggle.classList.remove("fa-eye-slash");
        confirmPasswordToggle.classList.add("fa-eye");
    }
}

function openProfilePictureModal() {
    $('#profilePictureModal').modal('show');
}

function closeProfilePictureModal() {
    $('#profilePictureModal').modal('hide');
}

function selectProfilePicture() {
    const selectedPicture = document.querySelector('input[name="profile_picture_modal"]:checked').value;
    const selectedPictureImg = document.querySelector('input[name="profile_picture_modal"]:checked').nextElementSibling.src;
    document.getElementById("selectedProfilePicture").src = selectedPictureImg;
    document.getElementById("profilePictureInput").value = selectedPicture;
    closeProfilePictureModal();
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    const profilePictureModal = $('#profilePictureModal');
    if (event.target == profilePictureModal[0]) {
        closeProfilePictureModal();
    }
}

function openDeleteAccountModal() {
    $('#deleteAccountModal').modal('show');
}

function closeDeleteAccountModal() {
    $('#deleteAccountModal').modal('hide');
}

function deleteAccount() {
    const message = "This feature is not available yet";
    alert(message);
    closeDeleteAccountModal();
    // Perform account deletion logic here
    // Redirect or perform any necessary actions after deletion
}
