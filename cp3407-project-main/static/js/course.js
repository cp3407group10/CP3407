document.addEventListener('DOMContentLoaded', function() {
    // Check login status when the page loads
    checkLoginStatus();
});

function checkLoginStatus() {
    fetch('/check_login_status')
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                // If not logged in, redirect to login page
                alert('Please log in to access this page.');
                window.location.href = '/login';
            } else {
                // Perform other checks
                checkEmptyCourses();
                checkAvailableCourses();
            }
        })
        .catch(error => {
            console.error('Error checking login status:', error);
        });
}

function checkEmptyCourses() {
    const joinedCourses = document.getElementById('created-courses').querySelectorAll('.course');
    const noCoursesMessage = document.getElementById('no-courses-message');
    if (joinedCourses.length === 0) {
        noCoursesMessage.style.display = 'block';
    } else {
        noCoursesMessage.style.display = 'none';
    }
}

function checkAvailableCourses() {
    const availableCourses = document.getElementById('available-courses').querySelectorAll('.course');
    const noAvailableCoursesMessage = document.getElementById('no-available-courses-message');
    if (availableCourses.length === 0) {
        noAvailableCoursesMessage.style.display = 'block';
    } else {
        noAvailableCoursesMessage.style.display = 'none';
    }
}

function joinSession(button) {
    const courseName = button.parentElement.getAttribute('data-course-name');

    fetch('/join_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'course_name': courseName
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Successfully joined the course!');
                // Create a new course element for the joined courses section
                const joinedCoursesContainer = document.getElementById('created-courses');
                const courseDiv = document.createElement('div');
                courseDiv.className = 'course course-' + courseName.replace(' ', '_').toLowerCase();
                courseDiv.setAttribute('data-course-name', courseName);
                courseDiv.innerHTML = `
                    <h3>${courseName}</h3>
                    <p>${data.course_content}</p>
                    <button class="leave" onclick="leaveSession(this)">Leave Session</button>
                `;
                joinedCoursesContainer.appendChild(courseDiv);

                // Hide the "no courses" message if needed
                document.getElementById('no-courses-message').style.display = 'none';

                // Remove the course from available courses
                button.parentElement.remove();

                // Show the "no available courses" message if needed
                checkAvailableCourses();
            } else {
                alert('Failed to join the course. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error joining course:', error);
            alert('An error occurred. Please try again.');
        });
}

function leaveSession(button) {
    const courseName = button.parentElement.getAttribute('data-course-name');

    fetch('/leave_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'course_name': courseName
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Successfully left the course!');
                // Remove the course element from the DOM
                const courseElement = button.parentElement;
                courseElement.remove();

                // Show the "no courses" message if there are no remaining courses
                checkEmptyCourses();
            } else {
                alert('Failed to leave the course. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error leaving course:', error);
            alert('An error occurred. Please try again.');
        });
}
