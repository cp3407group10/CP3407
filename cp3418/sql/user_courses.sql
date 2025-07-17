CREATE DATABASE IF NOT EXISTS user_information;
USE user_information;

CREATE TABLE IF NOT EXISTS user_courses (
                                            email VARCHAR(100) NOT NULL,
                                            course_name VARCHAR(100) NOT NULL,
                                            PRIMARY KEY (email, course_name)
);

