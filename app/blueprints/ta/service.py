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


