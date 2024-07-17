import mysql.connector
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)


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
    with open('about.html.', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route("/course")
def course():
    with open("course.html", encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/contact')
def contact():
    with open('contact.html.', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/login')
def login():
    with open('login.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


# processing requests submitted by the registration interface
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

            # Generate the registration success page with a login button
            success_html = """
                <h1>Registration Successful</h1>
                <p>Thank you for registering, {fullname}!</p>
                <a href="{login_url}"><button>Go to Login</button></a>
            """.format(fullname=fullname, login_url=url_for('login'))

            return success_html

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template_string(open('register.html').read())


@app.route('/logout')
def logout():
    with open('logout.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


# Redirect to the register route when accessing the root URL
@app.route('/')
def redirect_to_register():
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)