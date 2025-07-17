document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("signup-modal");
    const signupLink = document.getElementById("signup-link");
    const closeBtn = document.getElementsByClassName("close")[0];

    signupLink.onclick = function() {
        modal.style.display = "block";
    }

    closeBtn.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
