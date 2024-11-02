from flask import Blueprint, jsonify
from app.config import get_db_connection
import mysql.connector

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
                cursor.execute(command)

        conn.commit()  # Commit the transaction
        return jsonify({"status": "Tables created successfully."}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()