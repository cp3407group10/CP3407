function login() {
    const username = document.getElementById("username");
    const password = document.getElementById("password");

    if (username.value === "") {
        alert("Please enter username");
    } else if (password.value === "") {
        alert("Please enter password");
    } else if (username.value === "admin" && password.value === "123456") {
        window.location.href = "welcome.html";
    } else {
        alert("Please enter correct username and password！");
    }
}
