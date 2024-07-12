import cgi
import mysql.connector

# 连接到数据库
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Songjiahao4396",
    database="user_information"
)
print("Database connection successful.")


form = cgi.FieldStorage()
fullname = "John Doe"
email = "john.doe@example.com"
phone = "1234567890"
username = "johndoe"
password = "secure_password"
address = "123 Main St"
city = "Anytown"
zip_code = "12345"
# fullname = form.getvalue('fullname')
# email = form.getvalue('email')
# phone = form.getvalue('phone')
# username = form.getvalue('username')
# password = form.getvalue('password')
# address = form.getvalue('address')
# city = form.getvalue('city')
# zip_code = form.getvalue('zip')
print("get form")


cursor = db_connection.cursor()
insert_query = """
    INSERT INTO users (fullname, email, password, username, address, city, zip)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
insert_values = (fullname, email, password, username, address, city, zip_code)
cursor.execute(insert_query, insert_values)


db_connection.commit()


db_connection.close()


print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Registration Successful</title>")
print("</head>")
print("<body>")
print("<h2>Registration Successful</h2>")
print("<p>Thank you for registering.</p>")
print("</body>")
print("</html>")