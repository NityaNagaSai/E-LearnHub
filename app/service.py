from app.config import get_db_connection
from app.models import User

def validate_user(user_id, password, role):
    conn = get_db_connection()
    print("Inside validate user",conn)
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM User WHERE user_id = %s AND password = %s AND role = %s"
        cursor.execute(query, (user_id, password, role))
        user_data = cursor.fetchall()
        if user_data:
            if len(user_data) == 1:
                return True
            else:
                return False
        return None
    finally:
        cursor.close()
        conn.close()