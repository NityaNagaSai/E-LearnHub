import pymysql

# Define connection parameters
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = '1234'
DATABASE = 'elearnhub'
PORT = 3306

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