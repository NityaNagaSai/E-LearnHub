# import mariadb

# # Define connection parameters
# HOST = '127.0.0.1'
# USER = 'natluri'
# PASSWORD = '200536835'
# DATABASE = 'natluri'
# PORT = 3306

# # Establish a connection
# def get_db_connection():
#     try:
#         conn = mariadb.connect(
#             host=HOST,
#             user=USER,
#             password=PASSWORD,
#             database=DATABASE,
#             port=PORT,
#             local_infile=True  # Enable local_infile
#         )
#         print("Connected Successfully to MariaDB!")
#         return conn
#     except mariadb.Error as err:
#         print(f"Error: {err}")

# # Uncomment to test the connection
# connection = get_db_connection()
# if connection:
#     # Close connection after testing
#     connection.close()
