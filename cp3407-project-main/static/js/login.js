document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password-field').value;
    const errorMessage = document.getElementById('error-message');

    if (!email || !password) {
        errorMessage.textContent = 'Please enter your username and password';
        return;
    }

    // Simulate password validation
    if (password !== 'correct-password') { // Replace with actual password validation logic
        errorMessage.textContent = 'Incorrect Password';
        document.getElementById('password-field').value = ''; // Clear the password field
    } else {
        window.location.href = 'index.html'; // Redirect to homepage on success
    }
});

document.getElementById('toggle-password').addEventListener('click', function () {
    const passwordField = document.getElementById('password-field');
    const eyeIcon = document.getElementById('toggle-password');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        eyeIcon.src = 'static/images/no-eye-icon.png'; // Ensure you have this icon
    } else {
        passwordField.type = 'password';
        eyeIcon.src = 'static/images/eye-icon.png';
    }
});

// Modal logic
const modal = document.getElementById('signupModal');
const btn = document.getElementById('sign-up');
const span = document.getElementsByClassName('close')[0];

btn.onclick = function () {
    modal.style.display = 'block';
    modal.classList.add('slide-down'); // Add sliding effect class
}

span.onclick = function () {
    modal.style.display = 'none';
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
