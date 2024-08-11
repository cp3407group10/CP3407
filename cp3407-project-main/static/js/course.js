document.addEventListener('DOMContentLoaded', function () {
    const courses = document.querySelectorAll('.course');
    courses.forEach(course => {
        course.addEventListener('click', function (event) {
            // Check if the clicked element is not the button
            if (event.target.tagName !== 'BUTTON') {
                const url = this.dataset.url;
                window.location.href = url;
            }
        });
    });
});

function checkLoginStatus() {
    fetch('/check_login_status')
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                alert('Please log in to access this page.');
                window.location.href = '/login';
            } else {
                checkEmptyCourses();
                checkAvailableCourses();
            }
        })
        .catch(error => {
            console.error('Error checking login status:', error);
        });
}

function checkEmptyCourses() {
    const noCoursesMessage = document.getElementById('no-courses-message');
    if (!noCoursesMessage) {
        console.error('Element with ID "no-courses-message" not found.');
        return;
    }

    const joinedCourses = document.getElementById('created-courses').querySelectorAll('.course');
    noCoursesMessage.style.display = joinedCourses.length === 0 ? 'block' : 'none';
}

function checkAvailableCourses() {
    const noAvailableCoursesMessage = document.getElementById('no-available-courses-message');
    if (!noAvailableCoursesMessage) {
        console.error('Element with ID "no-available-courses-message" not found.');
        return;
    }

    const availableCourses = document.getElementById('available-courses').querySelectorAll('.course');
    noAvailableCoursesMessage.style.display = availableCourses.length === 0 ? 'block' : 'none';
}

function joinSession(button) {
    const courseName = button.parentElement.getAttribute('data-course-name');
    console.log('Joining session for course:', courseName);

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

                const noCoursesMessage = document.getElementById('no-courses-message');
                if (noCoursesMessage) {
                    noCoursesMessage.style.display = 'none';
                }

                button.parentElement.remove();
                checkAvailableCourses();
            } else {
                alert('Failed to join the course. Please try again, may be you have been selected this course');
            }
        })
        .catch(error => {
            console.error('Error joining course:', error);
            alert(`An error occurred. Please try again. Error: ${error.message}`);
        });
}

function leaveSession(button) {
    const courseName = button.parentElement.getAttribute('data-course-name');
    console.log('Leaving session for course:', courseName);

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
                button.parentElement.remove();
                checkEmptyCourses();
            } else {
                alert('Failed to leave the course. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error leaving course:', error);
            alert(`An error occurred. Please try again. Error: ${error.message}`);
        });
}
