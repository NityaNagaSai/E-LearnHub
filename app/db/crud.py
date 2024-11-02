from flask import Blueprint, jsonify
# from app.config import get_db_connection
from app.db_connect import get_db_connection
import mysql.connector

db_bp = Blueprint('db', __name__)

def create_tables():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to database."}), 500

    cursor = conn.cursor()

    try:
        # Read the SQL commands from the file
        with open('../E-LearnHub/db/create_tables.sql', 'r') as file:
            sql_commands = file.read().split(';')  # Split commands by semicolon

        # Execute each command
        for command in sql_commands:
            command = command.strip()  # Remove any leading/trailing whitespace
            if command:  # Check if the command is not empty
                if command.upper().startswith("CREATE TABLE"):
                    # Extract the table name and print it
                    table_name = command.split()[5].strip('`')
                    print(f"Creating table: {table_name}")
                cursor.execute(command)
        conn.commit()  # Commit the transaction
        print("Tables created successfully")
        return jsonify({"status": "Tables created successfully."}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

def insert_users():
    try:
        # Open the file and connect to the database
        with open('../E-LearnHub/db/users.txt', 'r') as file:
            conn = get_db_connection()
            if conn is None:
                return jsonify({"error": "Failed to connect to database."}), 500
            
            cursor = conn.cursor()
            query = '''
                INSERT INTO User (user_id, first_name, last_name, email, user_password, user_role)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            
            # Read and insert each line
            for line in file:
                data = line.strip().replace('"', '').split(', ')
                if len(data) == 6:  # Ensure line has exactly six fields
                    user_id, firstname, lastname, email, password, role = data
                    cursor.execute(query, (user_id, firstname, lastname, email, password, role))
                else:
                    print(f"Skipping malformed line: {line}")
            
            # Commit and close connection
            conn.commit()
            cursor.close()
            conn.close()
            print("Data inserted successfully")
        return "User data inserted successfully!"
    
    except Exception as e:
        return f"An error occurred: {e}"

# for inserting data
def populate_tables():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to database."}), 500
    try:
        with open('../E-LearnHub/db/populate_tables.sql', 'r') as file:
            sql_commands = file.read().split(';')  # Split commands by semicolon
        cursor = conn.cursor()
        for command in sql_commands:
            command = command.strip()
            if command:  # Check if the command is not empty
                try:
                    cursor.execute(command)
                    conn.commit()  # Commit the transaction
                    print(f"Executed command: {command}")
                except mysql.connector.Error as err:
                    print(f"Error executing command: {command}")
                    print(f"Error: {str(err)}")  # Log the error message

        print("Data inserted to tables successfully")
        return jsonify({"status": "Data inserted to tables successfully."}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()