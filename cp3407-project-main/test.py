import unittest
from flask import Flask, session
from app import app, db_config
import mysql.connector
from werkzeug.security import generate_password_hash


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.create_test_user()

    def create_test_user(self):
        try:
            db_connection = mysql.connector.connect(**db_config)
            cursor = db_connection.cursor()

            check_query = "SELECT email FROM users WHERE email=%s"
            cursor.execute(check_query, ('jiahao.Song@my.jcu.edu.au',))
            existing_user = cursor.fetchone()

            if not existing_user:
                hashed_password = generate_password_hash('123456')
                insert_query = """
                    INSERT INTO users (fullname, email, phone, username, password, address, city, zip)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, ('jiahao Song', 'jiahao.Song@my.jcu.edu.au', '83149559', 'jc943384', hashed_password, 'Eight Riversuites', '338521', '12345'))
                db_connection.commit()

            cursor.close()
            db_connection.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_about(self):
        result = self.app.get('/about')
        self.assertEqual(result.status_code, 200)

    def test_login(self):

        result = self.app.post('/login', data=dict(email='jiahao.Song@my.jcu.edu.au', password='123456'), follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Courses I Joined", result.data)

    def test_register(self):
        result = self.app.post('/register', data=dict(
            fullname='Unique User',
            email='uniqueuser@example.com',
            phone='1234567890',
            username='uniqueuser',
            password='password',
            address='123 Test St',
            city='Testville',
            zip='12345'
        ), follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Registration Successful", result.data)


if __name__ == '__main__':
    unittest.main()
