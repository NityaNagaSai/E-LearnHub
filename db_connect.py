import pymysql

# Define connection parameters
HOST = 'classdb2.csc.ncsu.edu'
USER = input("user_name:")
PASSWORD = input("password:")
DATABASE = input("database_name:")
PORT = 3306

# Establish a connection
try:
    conn = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,  # Specify the schema
            port=PORT  # Specify the port if not default
        )
    print("connected Successfully!")
    # if conn.is_connected():
except pymysql.MySQLError  as err:
    print(f"Error: {err}")
