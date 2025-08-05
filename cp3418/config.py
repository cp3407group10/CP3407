import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Songjiahao4396",
    "database": "user_information",
    "port": 3306,
    "auth_plugin": "mysql_native_password"
}
def get_db_connection():
    return mysql.connector.connect(**db_config)

