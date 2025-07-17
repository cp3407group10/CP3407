CREATE DATABASE IF NOT EXISTS user_information;
USE user_information;

CREATE TABLE IF NOT EXISTS courses (
                                       course_id INT AUTO_INCREMENT PRIMARY KEY,
                                       course_name VARCHAR(100) NOT NULL,
    course_content TEXT NOT NULL
    );

INSERT INTO courses (course_name, course_content) VALUES
                                                      ('Introduction to Python', 'This course covers the basics of Python programming language.'),
                                                      ('Data Structures and Algorithms', 'This course covers fundamental data structures and algorithms used in computer science.'),
                                                      ('Web Development', 'This course teaches the basics of web development using HTML, CSS, and JavaScript.'),
                                                      ('Database Systems', 'This course introduces the concepts of database systems, including SQL and NoSQL databases.'),
                                                      ('Operating Systems', 'This course covers the principles of operating systems, including process management and memory management.'),
                                                      ('Computer Networks', 'This course provides an overview of computer networking principles, protocols, and architectures.'),
                                                      ('Software Engineering', 'This course discusses software development methodologies, project management, and software design.'),
                                                      ('Artificial Intelligence', 'This course covers the basics of artificial intelligence, including machine learning and neural networks.'),
                                                      ('Cybersecurity', 'This course provides an introduction to cybersecurity principles, practices, and technologies.'),
                                                      ('Cloud Computing', 'This course discusses the concepts of cloud computing, including services like IaaS, PaaS, and SaaS.'),
                                                      ('Mobile App Development', 'This course covers the development of mobile applications for Android and iOS platforms.'),
                                                      ('Data Science', 'This course introduces the concepts and techniques of data science, including data analysis and visualization.'),
                                                      ('Game Development', 'This course covers the basics of game development, including game design and programming.'),
                                                      ('Machine Learning', 'This course provides an in-depth look at machine learning algorithms and applications.'),
                                                      ('Blockchain Technology', 'This course discusses the principles of blockchain technology and its applications.');
