CREATE DATABASE IF NOT EXISTS user_information;
USE user_information;

CREATE TABLE tokens (
                        token VARCHAR(255) PRIMARY KEY,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        expires_at DATETIME NULL,
                        status ENUM('active', 'used', 'expired') DEFAULT 'active'
);
