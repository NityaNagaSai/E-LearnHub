from app.config import get_db_connection
# from app.db_connect import get_db_connection
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
        query = '''INSERT INTO User(user_id, first_name, last_name, email, password, role) 
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

def add_etextbook_to_db(etextbook_id, title):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO ETextBook(textbook_id, title) 
                   VALUES(%s, %s)'''
        cursor.execute(query, (etextbook_id, title))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_etextbooks(etextbook_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM ETextBook WHERE textbook_id = %s"
        cursor.execute(query, (etextbook_id,))
        extextbook_data = cursor.fetchall()
        return extextbook_data
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# def update_etextbook(etextbook_id, title):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         query = '''UPDATE ETextbook
#                    SET title = %s
#                    WHERE textbook_id = %s;
#                 '''
#         cursor.execute(query, (title, etextbook_id))
#         conn.commit()
#         return True
#     except Error as e:
#         conn.rollback()
#         print(f"Error: {e}")
#         return False
#     finally:
#         cursor.close()
#         conn.close()

def add_chapter_to_db(chap_id, textbook_id, is_hidden, created_by, chap_title):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO Chapter(chapter_id, textbook_id, is_hidden, created_by, title) 
                   VALUES(%s, %s, %s, %s, %s)'''
        cursor.execute(query, (chap_id, textbook_id, is_hidden, created_by, chap_title))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_chapters(etextbook_id, chapter_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM Chapter WHERE textbook_id = %s and chapter_id = %s"
        cursor.execute(query, (etextbook_id, chapter_id,))
        chap_data = cursor.fetchall()
        print(etextbook_id+ " " + chapter_id)
        return chap_data
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def add_section_to_db(section_id, chap_id, textbook_id, is_hidden, created_by, sec_title):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO Section(section_id, textbook_id, chapter_id, title, is_hidden, created_by) 
                   VALUES(%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (section_id, textbook_id, chap_id, sec_title, is_hidden, created_by ))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_sections(etextbook_id, chapter_id, section_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM Section WHERE textbook_id = %s and chapter_id = %s and section_id = %s"
        cursor.execute(query, (etextbook_id, chapter_id, section_id))
        chap_data = cursor.fetchall()
        return chap_data
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def add_content_to_db(cb_id, section_id, chap_id, textbook_id, is_hidden, created_by, content_type, content):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO ContentBlock(content_block_id, textbook_id, section_id, chapter_id, content_type, 
                                       content, is_hidden, created_by) 
                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (cb_id, textbook_id, section_id, chap_id, content_type, content, is_hidden, created_by))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_content_blocks(etextbook_id, chapter_id, section_id, block_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM ContentBlock WHERE textbook_id = %s and chapter_id = %s and section_id = %s AND content_block_id = %s"
        cursor.execute(query, (etextbook_id, chapter_id, section_id, block_id))
        content_block__data = cursor.fetchall()
        return content_block__data
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_content_in_db(cb_id, section_id, chap_id, textbook_id, is_hidden, modified_by, content_type, modified_content):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''UPDATE ContentBlock 
                   SET content = %s, is_hidden = %s, created_by = %s, content_type = %s 
                   WHERE content_block_id = %s AND textbook_id = %s AND section_id = %s AND chapter_id = %s'''
        cursor.execute(query, (modified_content, is_hidden, modified_by, content_type, cb_id, textbook_id, section_id, chap_id))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def add_new_course(course_id, course_name, course_type, etextbook_id, faculty_id, start_date, end_date, unique_token, capacity):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO Course(course_id, course_title, course_type, faculty_user_id, 
                                        textbook_id, course_start_date, course_end_date, capacity, token) 
                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (course_id, course_name, course_type, faculty_id, etextbook_id, start_date, end_date, capacity, unique_token))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def add_activity_to_db(textbook_id, chapter_id, section_id, content_block_id, 
                                        activity_id, is_hidden, created_by):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO Activity(textbook_id, chapter_id, section_id, content_block_id, 
                                        activity_id, is_hidden, created_by) 
                   VALUES(%s, %s, %s, %s, %s, %s, %s)'''
        
        cursor.execute(query, (textbook_id, chapter_id, section_id, content_block_id, 
                                        activity_id, is_hidden, created_by))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_activity(textbook_id, chapter_id, section_id, content_block_id, activity_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''SELECT * FROM Activity WHERE textbook_id = %s AND chapter_id = %s AND 
                section_id = %s AND content_block_id = %s AND activity_id = %s'''
        cursor.execute(query, (textbook_id, chapter_id, section_id, content_block_id, activity_id))
        activity_data = cursor.fetchall()
        return activity_data
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def add_activity_question(question_id, activity_id, content_block_id, textbook_id, section_id, chapter_id, question, correct_answer, option1, option2, option3, option4, explanation_op1, explanation_op2, explanation_op3, explanation_op4):
    conn = get_db_connection()
    cursor = conn.cursor()
    print("inside add_activity_id method", textbook_id)
    try:
        query = '''INSERT INTO Question(question_id, activity_id, content_block_id, 
                                        textbook_id, section_id, chapter_id, question, 
                                        correct_answer, option1, option2, option3, 
                                        option4, explanation_op1, explanation_op2, 
                                        explanation_op3, explanation_op4) 
                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        
        cursor.execute(query, (question_id, activity_id, content_block_id, textbook_id, section_id, chapter_id, question, correct_answer, option1, option2, option3, option4, explanation_op1, explanation_op2, explanation_op3, explanation_op4))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_activity_questions(textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM Question WHERE textbook_id = %s and chapter_id = %s and section_id = %s and content_block_id = %s and activity_id = %s and question_id = %s;"
        cursor.execute(query, (textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id))
        questions_data = cursor.fetchall()
        # print(etextbook_id+ " " + chapter_id)
        return questions_data
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def delete_content(etextbook_id, chapter_id, section_id, content_block_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "DELETE FROM ContentBlock WHERE textbook_id = %s AND chapter_id = %s AND section_id = %s AND content_block_id = %s;"
        cursor.execute(query, (etextbook_id, chapter_id, section_id, content_block_id))
        # print(etextbook_id+ " " + chapter_id)
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
