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

def add_chapter_to_db(chap_id, textbook_id, is_hidden, created_by, chap_title):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO chapter(chapter_id, textbook_id, is_hidden, created_by, title) 
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
        query = "SELECT * FROM chapter WHERE textbook_id = %s and chapter_id = %s"
        cursor.execute(query, (etextbook_id, chapter_id,))
        chap_data = cursor.fetchall()
        return chap_data
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def add_section_to_db(section_id, chap_id, textbook_id, is_hidden, created_by, chap_title):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO chapter(section_id, chapter_id, textbook_id, is_hidden, created_by, title) 
                   VALUES(%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (section_id, chap_id, textbook_id, is_hidden, created_by, chap_title))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()