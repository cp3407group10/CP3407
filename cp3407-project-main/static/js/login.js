// 切换密码可见性
document.getElementById('toggle-password').addEventListener('click', function () {
    const passwordField = document.getElementById('password-field');
    const isPasswordVisible = passwordField.type === 'password';
    passwordField.type = isPasswordVisible ? 'text' : 'password';
    this.src = isPasswordVisible ? 'static/images/no-eye-icon.png' : 'static/images/eye-icon.png';
});


// 表单提交事件处理
document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password-field').value;
    const errorMessage = document.getElementById('error-message');

    if (!email || !password) {
        errorMessage.textContent = 'Please enter your username and password';
        return;
    }

    // 模拟密码验证，替换为服务器端验证
    if (password !== 'correct-password') {
        errorMessage.textContent = 'Incorrect Password';
        document.getElementById('password-field').value = '';
    } else {
        window.location.href = 'index.html';
    }
});

// 模态框逻辑
const modal = document.getElementById('signupModal');
document.getElementById('sign-up').addEventListener('click', () => {
    modal.style.display = 'block';
});
document.getElementsByClassName('close')[0].addEventListener('click', () => {
    modal.style.display = 'none';
});
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
