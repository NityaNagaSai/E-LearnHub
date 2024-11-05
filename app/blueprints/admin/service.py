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

def add_etextbook_to_db(etextbook_id, title):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO ETextbook(textbook_id, title) 
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
        query = "SELECT * FROM ETextbook WHERE textbook_id = %s"
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
        query = '''INSERT INTO Section(section_id, textbook_id, chapter_id, section_number, title, is_hidden, created_by) 
                   VALUES(%s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (section_id, textbook_id, chap_id, 101, sec_title, is_hidden, created_by ))
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
                                       content, sequence_number, is_hidden, created_by) 
                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (cb_id, textbook_id, section_id, chap_id, content_type, content, 101, is_hidden, created_by))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_content_in_db(cb_id, section_id, chap_id, textbook_id, is_hidden, modified_by, content_type, modified_content):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''UPDATE ContentBlock 
                   SET content = %s, is_hidden = %s, modified_by = %s, content_type = %s 
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
