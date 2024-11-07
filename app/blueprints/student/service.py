from app.config import get_db_connection
from app.models import User
# Student Enrollment
def enroll_student(first_name, last_name, email, password, course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        with conn.cursor() as cursor:
            # Check if the user already exists
            q1 = """
                SELECT user_id 
                FROM User 
                WHERE email = %s 
                AND first_name = %s AND
                last_name = %s
                """
            cursor.execute( q1, (email, first_name, last_name))
            result = cursor.fetchone()
            if result is None:
                first_day_of_current_month = datetime.now().replace(day=1)
                previous_month = first_day_of_current_month - timedelta(days=1)
                user_id = first_name[:2] + last_name[:2] + previous_month.strftime("%m%y")
                
                query = '''INSERT INTO User(user_id, first_name, last_name, email, password, role) 
                   VALUES(%s, %s, %s, %s, %s, %s)'''
                cursor.execute(query, (user_id, first_name, last_name, email, password, 'Student'))
                            # Create new user
                #             cursor.execute("""
                #                 INSERT INTO User (user_id, first_name, last_name, email, password, role)
                #                 VALUES (CONCAT(
                #     SUBSTRING(%s, 1, 2),
                #     SUBSTRING(%s, 1, 2),
                #     LPAD(MONTH(CURDATE()), 2, '0'),
                #     LPAD(YEAR(CURDATE()) % 100, 2, '0')
                # )%s, %s, %s, %s, %s, %s)
                #             """, (first_name, last_name, first_name, last_name, email, password, 'Student'))
                print("User created successfully.")
            
            # Check if the user already Enrolled or Pending
            cursor.execute(
                """
                SELECT e.status 
                FROM Enrollment e 
                JOIN User u ON u.user_id = e.student_user_id
                WHERE u.role = 'Student' AND
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

# Retrieve blocks and check content type is activity
def retrieve_blocks():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Fetch all blocks content, including activity check
        cursor.execute("""
         SELECT 
                et.textbook_id,
                et.title AS textbook_title,
                ch.chapter_id,
                ch.title AS chapter_title,
                sec.section_id,
                sec.title AS section_title,
                cb.content_block_id,
                cb.content_type,
                cb.content AS content_block_content,
                (cb.content_type = 'activity') AS is_activity
            FROM 
                ETextBook et
            JOIN 
                Chapter ch ON et.textbook_id = ch.textbook_id
            JOIN 
                Section sec ON ch.textbook_id = sec.textbook_id 
                             AND ch.chapter_id = sec.chapter_id
            JOIN 
                ContentBlock cb ON sec.textbook_id = cb.textbook_id 
                                AND sec.chapter_id = cb.chapter_id 
                                AND sec.section_id = cb.section_id
            WHERE 
                ch.is_hidden = 'no'
                AND sec.is_hidden = 'no'
                AND cb.is_hidden = 'no'
            ORDER BY 
                et.textbook_id, ch.chapter_id, sec.section_id, cb.content_block_id;
        """)

        content_blocks = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return content_blocks

# Retrieve All Questions
def retrieve_questions(textbook_id, chapter_id, section_id, content_block_id, activity_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Fetch questions for the specific activity
        cursor.execute("""
            SELECT 
                q.question_id,
                q.question,
                q.option1, q.explanation_op1,
                q.option2, q.explanation_op2,
                q.option3, q.explanation_op3,
                q.option4, q.explanation_op4,
                q.correct_answer
            FROM 
                Question q
            WHERE 
                q.textbook_id = %s 
                AND q.chapter_id = %s 
                AND q.section_id = %s 
                AND q.content_block_id = %s
                AND q.activity_id = %s
        """, (textbook_id, chapter_id, section_id, content_block_id, activity_id))
        questions = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return questions


def get_question_details(textbook_id, chapter_id, section_id, content_block_id, activity_id,question_id):
    """Retrieve question details from the database."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT question, explanation_op1,
             explanation_op2,explanation_op3, 
             explanation_op4, correct_answer
            FROM Question
            WHERE question_id = %s
            AND textbook_id = %s 
            AND chapter_id = %s 
            AND section_id = %s 
            AND content_block_id = %s
            AND activity_id = %s
        """, (question_id,textbook_id, chapter_id, section_id, content_block_id, activity_id))
        result = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    conn.close()
    return result

def save_student_activity_point(student_id, textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id, points, timestamp):
    """Insert or update the student activity point in the database."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO StudentActivityPoint (student_id, textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id, question_points, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE question_points = %s, timestamp = %s
        """, (student_id, textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id, points, timestamp, points, timestamp))
    conn.commit()
    conn.close()

def get_student_course_id(student_id):
    """Retrieve the course ID for the student's enrolled course."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT course_id
            FROM Enrollment
            WHERE student_user_id = %s AND status = 'Enrolled'
            LIMIT 1
        """, (student_id,))
        result = cursor.fetchone()
    conn.close()
    
    # Return the course_id if it exists, otherwise None
    return result[0] if result else None

def get_student_participation_points(student_id,course_id):
    """Retrieve student activity point in the database."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT sap.student_id, e.course_id, COUNT(sap.question_id) as finished_activites,
            SUM(sap.question_points) as participation_points from StudentActivityPoint sap
            INNER JOIN Enrollment e ON e.student_user_id = sap.student_id 
            WHERE e.status = 'Enrolled' and 
            sap.student_id = %s and
            e.course_id = %s
            GROUP BY sap.student_id, e.course_id;
        """, (student_id, course_id))
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result

def update_or_insert_student_participation(student_id, course_id):
    """Insert or update the student participation data in StudentParticipation."""
    # Retrieve participation points and finished activities
    student_data = get_student_participation_points(student_id, course_id)
    participation_points = student_data[3]
    finished_activities = student_data[2]
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Check if the record already exists in StudentParticipation
        cursor.execute("""
            SELECT 1 FROM StudentParticipation 
            WHERE student_id = %s AND course_id = %s
        """, (student_id, course_id))
        
        exists = cursor.fetchone()
        
        if exists:
            # Update the existing record
            cursor.execute("""
                UPDATE StudentParticipation
                SET participation_points = %s, finished_activities = %s
                WHERE student_id = %s AND course_id = %s
            """, (participation_points, finished_activities, student_id, course_id))
        else:
            # Insert a new record
            cursor.execute("""
                INSERT INTO StudentParticipation (student_id, course_id, participation_points, finished_activities)
                VALUES (%s, %s, %s, %s)
            """, (student_id, course_id, participation_points, finished_activities))
        
        # Commit changes and close the cursor and connection
        conn.commit()
        cursor.close()
    conn.close()


def get_student_participation_data(student_id, course_id):
    """Retrieve participation points and finished activities from StudentParticipation."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT participation_points, finished_activities
            FROM StudentParticipation
            WHERE student_id = %s AND course_id = %s
        """, (student_id, course_id))
        
        result = cursor.fetchone()
    
    conn.close()
    
    # Return a dictionary with default values if no data is found
    return {
        'participation_points': result[0] if result else 0,
        'finished_activities': result[1] if result else 0
    }
