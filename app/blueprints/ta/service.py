from app.config import get_db_connection
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

def check_active_course(course_id):
    """Check if the course with the given course_id is active and exists in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT course_id, course_title, textbook_id
            FROM Course
            WHERE course_id
            = %s AND course_type = 'Active'
        """
        cursor.execute(query, (course_id,))
        result = cursor.fetchone()
        return result if result else None
    except pymysql.MySQLError as e:
        print(f"Error checking active course: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def add_chapter_to_db(chap_id, textbook_id, is_hidden, created_by, chap_title):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO Chapter(chapter_id, textbook_id, is_hidden, created_by, title) 
                   VALUES(%s, %s, %s, %s, %s)'''
        cursor.execute(query, (chap_id, textbook_id, is_hidden, created_by, chap_title))
        conn.commit()
        return True
    except pymysql.Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_chapters(etextbook_id, chapter_id):
    """Fetch chapter details based on textbook and chapter IDs."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print(f"etextbook_id: {etextbook_id}, chapter_id: {chapter_id}")
        query = "SELECT * FROM Chapter WHERE textbook_id = %s AND chapter_id = %s"
        cursor.execute(query, (etextbook_id, chapter_id,))
        chapters = cursor.fetchall()
        return chapters
    except pymysql.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def add_section_to_db(section_id, chap_id, textbook_id, is_hidden, created_by, sec_title):
    """Add a new section to the Section table."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO Section (section_id, textbook_id, chapter_id, title, is_hidden, created_by)
                   VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (section_id, textbook_id, chap_id, sec_title, is_hidden, created_by))
        conn.commit()
        return True
    except pymysql.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

