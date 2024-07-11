<?php

$servername = "localhost";
$username = "your_username";
$password = "your_password";
$dbname = "user_registration";

$conn = new mysqli($servername, $username, $password, $dbname);


if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}


$sql = "INSERT INTO users (fullname, email, phone, username, password, address, city, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";


$stmt = $conn->prepare($sql);
$stmt->bind_param("ssssssss", $fullname, $email, $phone, $username, $password_hash, $address, $city, $zip);


$fullname = $_POST['fullname'];
$email = $_POST['email'];
$phone = $_POST['phone'];
$username = $_POST['username'];
$password = $_POST['password'];
$password_hash = password_hash($password, PASSWORD_DEFAULT); // 对密码进行哈希加密以提高安全性
$address = $_POST['address'];
$city = $_POST['city'];
$zip = $_POST['zip'];


if ($stmt->execute()) {
    echo "注册成功！";
} else {
    echo "错误: " . $sql . "<br>" . $conn->error;
}


$stmt->close();
$conn->close();
?>
