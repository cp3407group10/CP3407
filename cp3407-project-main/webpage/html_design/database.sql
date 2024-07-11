CREATE DATABASE IF NOT EXISTS user_name;
USE user_name;

CREATE TABLE IF NOT EXISTS users (
                                     id INT AUTO_INCREMENT PRIMARY KEY,
                                     fullname VARCHAR(100) NOT NULL,
                                     email VARCHAR(100) NOT NULL,
                                     phone VARCHAR(20)
);
