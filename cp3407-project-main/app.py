import mysql.connector
from flask import Flask, request, render_template_string, redirect, url_for,flash

app = Flask(__name__)

# Define database link information
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Songjiahao4396",
    "database": "user_information",
    "port": 3306
}

def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def render_template(file_path):
    return render_template_string(read_html(file_path))

@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_field = request.form['login_field']
        password = request.form['password']

        try:
            # Connect to the database and execute the select operation
            db_connection = mysql.connector.connect(**db_config)
            cursor = db_connection.cursor(dictionary=True)
            select_query = """
                SELECT * FROM users WHERE (email=%s OR phone=%s OR username=%s) AND password=%s
            """
            cursor.execute(select_query, (login_field, login_field, login_field, password))
            user = cursor.fetchone()
            cursor.close()
            db_connection.close()

            if user:
                return redirect(url_for('index'))  # Redirect to the index page upon successful login
            else:
                flash('Invalid login credentials')

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template_string(read_html('login.html'))

# processing requrests submitted by the registration interface
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form.get('phone', '')  # Use .get() to handle optional fields
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        city = request.form.get('city', '')  # Use .get() to handle optional fields
        zip_code = request.form.get('zip', '')  # Use .get() to handle optional fields

        try:
            # Connect to the database and execute the insert operation
            db_connection = mysql.connector.connect(**db_config)
            cursor = db_connection.cursor()
            insert_query = """
                INSERT INTO users (fullname, email, phone, username, password, address, city, zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_values = (fullname, email, phone, username, password, address, city, zip_code)
            cursor.execute(insert_query, insert_values)
            db_connection.commit()
            cursor.close()
            db_connection.close()

            return "Registration Successful"

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template_string(open('register.html').read())


@app.route('/about')
def about():
    return render_template('about.html')

# Route for course page
@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')






if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)