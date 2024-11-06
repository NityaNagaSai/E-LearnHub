import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user='root',               # Remote MySQL username
            password='Stupid!3198',         # Remote MySQL password
            host='127.0.0.1',             # Accessing via SSH tunnel on localhost
            port=3306,                    # The port you forwarded in PuTTY
            database='elearnhub'            # Database name on the remote server
        )

        return conn
    except mysql.connector.Error as err:
        print(err)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(err.errno)
            print("Database does not exist here.")
        else:
            print(err)

# import pymysql

# def get_db_connection():
#     try:
#         conn = pymysql.connect(
#             user='natluri',               # Remote MySQL username
#             password='200536835',         # Remote MySQL password
#             host='127.0.0.1',             # Accessing via SSH tunnel on localhost
#             port=3307,                    # The port you forwarded in PuTTY
#             database='natluri'            # Database name on the remote server
#         )
#         print("Connected to natluri database successfully!")
#         return conn
#     except pymysql.MySQLError as err:
#         print("Error:", err)
#         if err.args[0] == 1045:  # ER_ACCESS_DENIED_ERROR
#             print("Something is wrong with your username or password.")
#         elif err.args[0] == 1049:  # ER_BAD_DB_ERROR
#             print("Database does not exist.")
#         else:
#             print("An error occurred:", err)

# # Test the connection
# connection = get_db_connection()
# if connection:
#     connection.close()
