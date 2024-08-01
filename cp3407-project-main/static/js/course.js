document.addEventListener('DOMContentLoaded', function () {
    checkEmptyCourses();
    checkAvailableCourses();
});

function joinSession(button) {
    const course = button.closest('.course');
    const createdCoursesContainer = document.getElementById('created-courses');
    createdCoursesContainer.insertBefore(course, createdCoursesContainer.firstChild);
    button.textContent = 'Leave Session';
    button.classList.remove('join');
    button.classList.add('leave');
    button.onclick = function() { leaveSession(this); };

    // Optionally, make an AJAX call to the server to persist the change
    const courseId = course.getAttribute('data-course-id');
    fetch('/join_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ course_id: courseId }),
    });

    checkEmptyCourses();
    checkAvailableCourses();
}

function leaveSession(button) {
    const course = button.closest('.course');
    const availableCoursesContainer = document.getElementById('available-courses');
    availableCoursesContainer.insertBefore(course, availableCoursesContainer.firstChild);
    button.textContent = 'Join Session';
    button.classList.remove('leave');
    button.classList.add('join');
    button.onclick = function() { joinSession(this); };

    // Optionally, make an AJAX call to the server to persist the change
    const courseId = course.getAttribute('data-course-id');
    fetch('/leave_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ course_id: courseId }),
    });

    checkEmptyCourses();
    checkAvailableCourses();
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
