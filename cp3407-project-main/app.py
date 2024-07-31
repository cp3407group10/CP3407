import mysql.connector
from flask import Flask, request, render_template_string, redirect, url_for, session,flash

app = Flask(__name__)
app.secret_key = 'sjh123'

# Define database link information
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Songjiahao4396",
    "database": "user_information",
    "port": 3306
}


@app.route('/')
def index():
    with open('index.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/about')
def about():
    with open('about.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/course')
def course():
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("SELECT course_name, course_content FROM courses")
        courses = cursor.fetchall()

        cursor.close()
        db_connection.close()

        with open("course.html", encoding='utf-8') as f:
            html_content = f.read()

        return render_template_string(html_content, courses=courses)

    except mysql.connector.Error as err:
        return f"Error: {err}"


@app.route('/contact')
def contact():
    with open('contact.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Connect to the database and fetch user information
            db_connection = mysql.connector.connect(**db_config)
            cursor = db_connection.cursor()
            select_query = "SELECT * FROM users WHERE email=%s AND password=%s"
            cursor.execute(select_query, (email, password))
            user = cursor.fetchone()
            cursor.close()
            db_connection.close()

            # Debugging: print fetched user information
            print(f"Fetched user: {user}")

            if user:
                session['user'] = user  # Store user information in session
                return redirect(url_for('dashboard'))
            else:
                return "Invalid email or password. Please try again."

        except mysql.connector.Error as err:
            return f"Error: {err}"

    with open('login.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form.get('phone', '')
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        city = request.form.get('city', '')
        zip_code = request.form.get('zip', '')

        try:

            db_connection = mysql.connector.connect(**db_config)
            cursor = db_connection.cursor()


            check_query = "SELECT * FROM users WHERE email=%s"
            cursor.execute(check_query, (email,))
            existing_user = cursor.fetchone()


            cursor.fetchall()

            if existing_user:
                #
                flash("This email is already registered. Please use a different email.", 'error')
                cursor.close()
                db_connection.close()
                return redirect(url_for('register'))


            insert_query = """
                INSERT INTO users (fullname, email, phone, username, password, address, city, zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_values = (fullname, email, phone, username, password, address, city, zip_code)
            cursor.execute(insert_query, insert_values)
            db_connection.commit()

            cursor.close()
            db_connection.close()


            success_html = """
                <h1>Registration Successful</h1>
                <p>Thank you for registering, {fullname}!</p>
                <a href="{login_url}"><button>Go to Login</button></a>
            """.format(fullname=fullname, login_url=url_for('login'))

            return success_html

        except mysql.connector.Error as err:
            return f"Error: {err}"

    with open('register.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    with open('logout.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user']
        return f"Welcome {user[1]}! You are logged in."
    return redirect(url_for('login'))

# Redirect to the register route when accessing the root URL
@app.route('/redirect_to_register')
def redirect_to_register():
    return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)