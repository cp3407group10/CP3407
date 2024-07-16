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


@app.route('/')
def index():
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)