from app.db_connect import get_db_connection
from app.models import User
import pymysql

# fetch courses
def fetch_courses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT course_id, course_title from Course
            WHERE ta_user_id = %s;
        """
        cursor.execute(query, (user_id))
        result = cursor.fetchall()
        print(result)
        conn.commit()
        return result
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# fetch enrolled students of a active course
def fetch_students(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
                SELECT CONCAT(u.first_name, ' ', u.last_name) as student_name
                from Course c
                INNER JOIN Enrollment e
                ON c.course_id = e.course_id 
                AND c.course_type = "Active"
                INNER JOIN User u
                ON e.student_user_id = u.user_id
                AND e.status = "Enrolled"
                AND u.role = "Student"
                WHERE c.course_id = %s;
                """
        cursor.execute(query, (course_id))
        result = cursor.fetchall()
        print(result)
        conn.commit()
        return result
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def validate_current_password(user_id, current_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Fetch the stored password for the user
        query = "SELECT password FROM User WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        if result:
            stored_password = result[0]
            print(f"Stored password for user {user_id}: {stored_password}")
            print(f"Entered password for user {user_id}: {current_password}")

            # Directly compare stored password with the entered password
            password_matches = stored_password == current_password
            print(f"Password match result: {password_matches}")
            return password_matches
        else:
            print(f"No result found for user_id: {user_id}")
            return False
    except Exception as e:
        print(f"Error validating password: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def update_user_password(user_id, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Use the new password directly as plain text
        query = "UPDATE User SET password = %s WHERE user_id = %s"
        cursor.execute(query, (new_password, user_id))
        conn.commit()
        
        print("Password updated successfully.")
        return True
    finally:
        cursor.close()
        conn.close()



