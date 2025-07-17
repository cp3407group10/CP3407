// validateForm.js

function validateForm() {
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;
    const error_message = document.getElementById("password_error");

    if (password !== confirm_password) {
        error_message.textContent = "The two passwords are different";
        return false;
    } else {
        error_message.textContent = "";
        return true;
    }
}
