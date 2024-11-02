from app.config import get_db_connection
from app.models import User
from datetime import datetime, timedelta
from mysql.connector import Error

def create_new_faculty_account(first_name, last_name, email, password):
    first_day_of_current_month = datetime.now().replace(day=1)

    previous_month = first_day_of_current_month - timedelta(days=1)
    user_id = first_name[:2] + last_name[:2] + previous_month.strftime("%m%y")
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO User(user_id, first_name, last_name, email, user_password, user_role) 
                   VALUES(%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (user_id, first_name, last_name, email, password, 'Faculty'))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()