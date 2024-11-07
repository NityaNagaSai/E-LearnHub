from app.config import get_db_connection
from app.models import User
from mysql.connector import Error


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

def retrieval_sql_query1(textbook_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''SELECT COUNT(*) AS number_of_sections
                   FROM Section s
                   WHERE s.textbook_id = %s AND s.chapter_id = %s;'''
        
        cursor.execute(query, (textbook_id, "chap01"))
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def retrieval_sql_query2():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''SELECT U.first_name, U.last_name, 'Faculty' AS role
                    FROM Course C
                    JOIN User U ON C.faculty_user_id = U.user_id
                    UNION
                    SELECT U.first_name, U.last_name, 'TA' AS role
                    FROM Course C
                    JOIN User U ON C.ta_user_id = U.user_id;
                '''
        
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
    
def retrieval_sql_query3():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''SELECT C.course_id, CONCAT(U.first_name, ' ', U.last_name) AS faculty_name, COUNT(E.student_user_id) AS total_students
                    FROM Course C
                    JOIN User U ON C.faculty_user_id = U.user_id
                    LEFT JOIN Enrollment E ON C.course_id = E.course_id AND E.status = 'Enrolled'
                    WHERE C.course_type = 'Active'
                    GROUP BY C.course_id, faculty_name;
                '''
        
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def retrieval_sql_query4():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''
                    SELECT C.course_id, COUNT(*) AS waiting_list_count
                    FROM Enrollment E
                    JOIN Course C ON E.course_id = C.course_id
                    WHERE E.status = 'Pending'
                    GROUP BY C.course_id
                    ORDER BY waiting_list_count DESC
                    LIMIT 1;
                '''
        
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
    
def retrieval_sql_query5():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = ''' SELECT CB.content
                    FROM ContentBlock CB
                    WHERE CB.textbook_id = 101 AND CB.chapter_id = 'Chap02'
                    ORDER BY CB.section_id, CB.content_block_id;
                '''
        
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
            
def retrieval_sql_query6():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''SELECT Q.option1, Q.explanation_op1, Q.option2, Q.explanation_op2, 
                    Q.option3, Q.explanation_op3, Q.option4, Q.explanation_op4, Q.correct_answer
                    FROM Question Q
                    WHERE Q.textbook_id = 101 AND Q.chapter_id = 'chap01' 
                        AND Q.section_id = 'Sec02' AND Q.content_block_id = 'Block01' 
                        AND activity_id = 'ACT0'
                        AND Q.question_id = 'Q2'
                    AND Q.correct_answer NOT IN (Q.option1, Q.option2, Q.option3, Q.option4);
                '''
        
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            options = [
                (1, result[0], result[1]),  # option1 and explanation_op1
                (2, result[2], result[3]),  # option2 and explanation_op2
                (3, result[4], result[5]),  # option3 and explanation_op3
                (4, result[6], result[7])   # option4 and explanation_op4
            ]
            correct_answer = result[8]
            return options, correct_answer
        else:
            return None, None
    
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
                
def retrieval_sql_query7():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''SELECT C1.textbook_id
                    FROM Course C1
                    JOIN Course C2 ON C1.textbook_id = C2.textbook_id 
                        AND C1.course_type = 'Active' AND C2.course_type = 'Evaluation'
                        AND C1.faculty_user_id != C2.faculty_user_id;
                '''
        #
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
