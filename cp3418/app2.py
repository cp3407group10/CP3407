from flask import Flask, render_template_string, request, redirect, url_for, session, flash, jsonify
from qr_auth import qr_bp
from config import db_config
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sjh123'

# 注册扫码登录蓝图
app.register_blueprint(qr_bp)

@app.route('/')
def index():
    with open('templates/index.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/about')
def about():
    with open('templates/about.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/contact')
def contact():
    with open('templates/contact.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('Name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    satisfaction = request.form.get('reference')
    preferred_date = request.form.get('preferredDate')
    preferred_time = request.form.get('preferredTime')
    comments = request.form.get('comments')

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        insert_query = """
            INSERT INTO feedback (name, email, phone, satisfaction, preferred_date, preferred_time, comments)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        insert_values = (name, email, phone, satisfaction, preferred_date, preferred_time, comments)
        cursor.execute(insert_query, insert_values)
        db_connection.commit()

        cursor.close()
        db_connection.close()

        with open('templates/success.html', encoding='utf-8') as f:
            success_html_content = f.read()

        return render_template_string(success_html_content)

    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'error')
        return redirect(url_for('contact'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            db_connection = mysql.connector.connect(**db_config)
            cursor = db_connection.cursor(dictionary=True)
            select_query = "SELECT id, email, password, fullname FROM users WHERE email=%s"
            cursor.execute(select_query, (email,))
            user = cursor.fetchone()
            cursor.close()
            db_connection.close()

            if user and check_password_hash(user['password'], password):
                session['user'] = {
                    'id': user['id'],
                    'email': user['email'],
                    'fullname': user['fullname']
                }
                return redirect(url_for('course'))
            else:
                flash("Invalid email or password. Please try again.", 'error')
                return redirect(url_for('login'))

        except mysql.connector.Error as err:
            return f"Error: {err}"

    with open('templates/login.html', encoding='utf-8') as f:
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

            # Check if email already exists
            check_query = "SELECT email FROM users WHERE email=%s"
            cursor.execute(check_query, (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("This email is already registered. Please use a different email.", 'error')
                cursor.close()
                db_connection.close()
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password)
            insert_query = """
                INSERT INTO users (fullname, email, phone, username, password, address, city, zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_values = (fullname, email, phone, username, hashed_password, address, city, zip_code)
            cursor.execute(insert_query, insert_values)
            db_connection.commit()

            cursor.close()
            db_connection.close()

            success_html = """
                <h1>Registration Successful</h1>
                <p>Thank you for registering, {{ fullname }}!</p>
                <a href="{{ login_url }}"><button>Go to Login</button></a>
            """
            return render_template_string(success_html, fullname=fullname, login_url=url_for('login'))

        except mysql.connector.Error as err:
            return f"Error: {err}"

    with open('templates/register.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", 'info')
    with open('templates/logout.html', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user']
        return render_template_string(f'''
            <h1>欢迎, {user["fullname"]}!</h1>
            <p>你的邮箱是: {user["email"]}</p>
            <a href="{url_for("logout")}">注销</a>
        ''')
    return redirect(url_for('login'))


@app.route('/redirect_to_register')
def redirect_to_register():
    return redirect(url_for('register'))


@app.route('/check_login_status')
def check_login_status():
    return jsonify({'logged_in': 'user' in session})


@app.route('/course')
def course():
    if 'user' not in session:
        return redirect(url_for('login'))

    email = session['user']['email']

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("SELECT course_id, course_name, course_content FROM courses")
        courses = cursor.fetchall()

        cursor.execute("""
            SELECT c.course_id, c.course_name, c.course_content 
            FROM courses c
            JOIN user_courses uc ON c.course_name = uc.course_name
            WHERE uc.email = %s
        """, (email,))
        joined_courses = cursor.fetchall()

        cursor.close()
        db_connection.close()

        with open("templates/course.html", encoding='utf-8') as f:
            html_content = f.read()

        return render_template_string(html_content, courses=courses, joined_courses=joined_courses)

    except mysql.connector.Error as err:
        return f"Error: {err}"


@app.route('/join_course', methods=['POST'])
def join_course():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'You need to be logged in to join a course.'})

    email = session.get('user', {}).get('email')
    if not email:
        return jsonify({'success': False, 'message': 'User information is incomplete. Please log in again.'})

    course_name = request.form.get('course_name')
    if not course_name:
        return jsonify({'success': False, 'message': 'Course name is required.'})

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        cursor.execute("SELECT * FROM courses WHERE course_name = %s", (course_name,))
        course = cursor.fetchone()
        if not course:
            cursor.close()
            db_connection.close()
            return jsonify({'success': False, 'message': 'Course not found.'})

        cursor.execute("SELECT * FROM user_courses WHERE email = %s AND course_name = %s", (email, course_name))
        existing_enrollment = cursor.fetchone()
        if existing_enrollment:
            cursor.close()
            db_connection.close()
            return jsonify({'success': False, 'message': 'You are already enrolled in this course.'})

        insert_query = "INSERT INTO user_courses (email, course_name) VALUES (%s, %s)"
        cursor.execute(insert_query, (email, course_name))
        db_connection.commit()

        cursor.close()
        db_connection.close()

        return jsonify({'success': True, 'course_content': course[2]})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': str(err)})


@app.route('/leave_course', methods=['POST'])
def leave_course():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'You need to be logged in to leave a course.'})

    email = session.get('user', {}).get('email')
    if not email:
        return jsonify({'success': False, 'message': 'User information is incomplete. Please log in again.'})

    course_name = request.form.get('course_name')
    if not course_name:
        return jsonify({'success': False, 'message': 'Course name is required.'})

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        cursor.execute("DELETE FROM user_courses WHERE email = %s AND course_name = %s", (email, course_name))
        db_connection.commit()

        cursor.close()
        db_connection.close()

        return jsonify({'success': True})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': str(err)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
