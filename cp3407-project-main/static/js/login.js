document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password-field').value;
    const errorMessage = document.getElementById('error-message');

    if (!email || !password) {
        errorMessage.textContent = 'Please enter your username and password';
        return;
    }

    // 模拟验证密码
    if (password !== 'correct-password') { // 替换为实际的密码验证逻辑
        errorMessage.textContent = 'Incorrect Password';
        document.getElementById('password-field').value = ''; // 清空密码输入框
    } else {
        window.location.href = 'index.html'; // 如果验证成功，跳转到主页
    }
});

document.getElementById('toggle-password').addEventListener('click', function () {
    const passwordField = document.getElementById('password-field');
    const eyeIcon = document.getElementById('toggle-password');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        eyeIcon.src = 'images/no-eye-icon.png'; // 确保你有这个图标
    } else {
        passwordField.type = 'password';
        eyeIcon.src = 'images/eye-icon.png';
    }
});

// 模态框相关逻辑
const modal = document.getElementById('signupModal');
const btn = document.getElementById('sign-up');
const span = document.getElementsByClassName('close')[0];

btn.onclick = function () {
    modal.style.display = 'block';
    modal.classList.add('slide-down'); // 添加滑动效果的类
}

span.onclick = function () {
    modal.style.display = 'none';
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
