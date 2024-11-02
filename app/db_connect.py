import pymysql

# Define connection parameters
HOST = '127.0.0.1'
USER = 'mgaddam'
PASSWORD = '200538368'
DATABASE = 'mgaddam'
PORT = 57664

# Establish a connection
def get_db_connection():
    try:
        conn = pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,  # Specify the schema
                port=PORT,  # Specify the port if not default
                local_infile=1
            )
        print("connected Successfully!")
        return conn
    except pymysql.MySQLError  as err:
        print(f"Error: {err}")
# get_db_connection()