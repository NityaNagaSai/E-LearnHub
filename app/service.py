# from app.config import get_db_connection
from app.db_connect import get_db_connection
from app.models import User

def validate_user(user_id, password, role):
    conn = get_db_connection()
    print("Inside validate user",conn)
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM User WHERE user_id = %s AND user_password = %s AND user_role = %s"
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

# Student Enrollment
def enroll_student(first_name, last_name, email, password, course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        with conn.cursor() as cursor:
            # Check if the user already exists
            cursor.execute(
                """
                SELECT user_id 
                FROM User 
                WHERE email = %s 
                AND first_name = %s AND
                last_name = %s
                """,
                (email, first_name, last_name)
            )
            result = cursor.fetchone()
            if result is None:
                # Create new user
                cursor.execute("""
                    INSERT INTO User (user_id, first_name, last_name, email, password, role)
                    VALUES (CONCAT(
        SUBSTRING(%s, 1, 2),
        SUBSTRING(%s, 1, 2),
        LPAD(MONTH(CURDATE()), 2, '0'),
        LPAD(YEAR(CURDATE()) % 100, 2, '0')
    ), %s, %s, %s, %s, %s)
                """, (first_name, last_name, first_name, last_name, email, password, 'Student'))
                print("User created successfully.")
            
            # Check if the user already Enrolled or Pending
            cursor.execute(
                """
                SELECT e.status 
                FROM Enrollment e 
                JOIN User u ON u.user_id = e.student_user_id
                WHERE u.user_role = 'Student' AND
                e.course_id = %s AND u.first_name = %s AND
                u.last_name = %s AND u.email = %s
                """,
                (course_id, first_name, last_name, email)
            )
            status = cursor.fetchone()
            if status is None:
                # Insert enrollment request
                cursor.execute("""
                INSERT IGNORE INTO Enrollment (course_id, student_user_id, status)
                VALUES (%s, (SELECT user_id FROM User WHERE email = %s
                AND first_name = %s AND
                last_name = %s), 'Pending')
                """, (course_id, email, first_name, last_name))
                conn.commit()
                print("Enrollment request recorded.")
                return "Created"
            else:
                return status[0]
    finally:
        cursor.close()
        conn.close()