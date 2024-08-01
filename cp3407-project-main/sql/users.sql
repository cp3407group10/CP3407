CREATE DATABASE IF NOT EXISTS user_information;
USE user_information;

CREATE TABLE IF NOT EXISTS users (
                                     id INT AUTO_INCREMENT PRIMARY KEY,
                                     fullname VARCHAR(100) NOT NULL ,
                                     email VARCHAR(100) NOT NULL ,
                                     phone VARCHAR(50) NOT NULL ,
                                     password VARCHAR(255) NOT NULL ,
                                     username VARCHAR(50) NOT NULL ,
                                     address VARCHAR(255),
                                     city VARCHAR(100),
                                     zip VARCHAR(20)
);





