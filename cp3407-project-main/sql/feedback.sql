CREATE DATABASE IF NOT EXISTS user_information;
USE user_information;
CREATE TABLE feedback (
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          name VARCHAR(255) NOT NULL,
                          email VARCHAR(255) NOT NULL,
                          phone VARCHAR(50),
                          satisfaction VARCHAR(50),
                          preferred_date DATE,
                          preferred_time TIME,
                          comments TEXT,
                          submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
