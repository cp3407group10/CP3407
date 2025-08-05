CREATE DATABASE IF NOT EXISTS user_information;
USE user_information;

CREATE TABLE IF NOT EXISTS auth_logs (
                                         id INT AUTO_INCREMENT PRIMARY KEY,
                                         token VARCHAR(255),
                                         reasons TEXT,
                                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


