import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user ='root',
            password = 'mysql1234',
            host = '127.0.0.1',
            port = '3306',
            database = 'elearnhub',
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
