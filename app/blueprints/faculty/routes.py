from flask import Blueprint, render_template, redirect, session, url_for, request, flash
from . import faculty_bp
import mysql.connector
from mysql.connector import errorcode
import logging
from app.blueprints.faculty.service import *

# Configure the logging module
logging.basicConfig(level=logging.DEBUG)

@faculty_bp.route('/home', methods=['GET', 'POST'])
def faculty_home():
    return render_template('faculty_landing.html')

# Route for 'Go to Active Course'
@faculty_bp.route('/active_course', methods=["GET", "POST"])
def go_to_active_course():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        option = request.form.get('option')
        session['course_id'] = course_id  # Save the selected course_id for later use
        course_list = check_course(course_id, 'Active' )
        
        if len(course_list) == 0:
            print("Please enter a valid Course ID", "error")
            return redirect(url_for('faculty.go_to_active_course'))

        # Redirect based on the selected option
        if option == '1':
            waitlisted_students = get_waitlisted_students(course_id)
            session['waitlist'] = waitlisted_students  # Store waitlist in session
            return redirect(url_for('faculty.view_worklist', course_id=course_id))
        elif option == '2':
            return redirect(url_for('faculty.approve_enrollment', course_id=course_id))
        elif option == '3':
            students = get_students(course_id)
            session['enrolled'] = students
            return redirect(url_for('faculty.view_students', course_id=course_id))
        elif option == '4':
            textbook_id = get_etextbook_id(course_id)
            if len(textbook_id) == 1:
                session["textbook_id"] = textbook_id[1]
            return redirect(url_for('faculty.add_chapter', course_id=course_id))
        elif option == '5':
            return redirect(url_for('faculty.modify_chapters', course_id=course_id))
        elif option == '6':
            return redirect(url_for('faculty.add_ta', course_id=course_id))
        elif option == '7':
            return redirect(url_for('faculty.faculty_home'))
        else:
            flash("Invalid option selected.", "error")
            return redirect(url_for('faculty.go_to_active_course'))
        
    return render_template('active_course.html')

@faculty_bp.route('/evaluation_course', methods=["GET", "POST"])
def go_to_evaluation_course():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        option = request.form.get('option')
        session['course_id'] = course_id  # Save the selected course_id for later use
        course_list = check_course(course_id, 'Evaluation' )
        
        if len(course_list) == 0:
            print("Please enter a valid Course ID", "error")
            return redirect(url_for('faculty.go_to_evaluation_course'))
        if option == '1':
            return redirect(url_for('faculty.add_chapter', course_id=course_id))
        elif option == '2':
            return redirect(url_for('modify_chapters', course_id=course_id))
        elif option == '3':
            return redirect(url_for('faculty.faculty_home'))
        else:
            flash("Invalid option selected.", "error")
            return redirect(url_for('faculty.go_to_evaluation_course'))
    return render_template('evaluation_course.html')  # Replace with your template

# Route for 'View Courses'
@faculty_bp.route('/view_courses')
def view_courses():
   assigned_courses = [{"couseID" : "CSC 540", "name": "CSC 540 DBMS"},
                       {"couseID" : "CSC 591 A", "name":"CSC 591 ML with Graphs"} , 
                       {"couseID" : "CSC 591 B", "name":"CSC 591 Programmer Centered Design and Research"}]

   if request.method == 'POST':
   #Query Courses from DB and send it
   # assigned_courses = Course.query.filter_by(faculty_id=faculty_id).all()
    option = request.form.get('option')
    
    if option == '1':
        return redirect(url_for('faculty.faculty_home'))
    else:
        flash("Invalid option selected.", "error")
        return redirect(url_for('go_to_active_course'))
   return render_template('view_courses.html', courses=assigned_courses)  # Replace with your template

@faculty_bp.route('/view_students/<course_id>', methods=["GET", "POST"])
def view_students(course_id):
    student_list = session.get('enrolled')  
    print(student_list)
    return render_template('view_student_list.html', student_list=student_list, courseID=course_id)

@faculty_bp.route('/approve_enrollment/<course_id>')
def approve_enrollment(course_id):
    return render_template('approve_enrollment.html', course_id = course_id)

@faculty_bp.route('/add_chapter/<course_id>')
def add_chapter(course_id):
    text_tuple = get_etextbook_id(course_id)
    etextbook_id, etextbook_title = text_tuple[0], text_tuple[1]
    session['etextbook_id'] = etextbook_id
    return render_template('faculty_add_chapter.html', etextbook_title=etextbook_title, etextbook_id=etextbook_id, call_type="new")

@faculty_bp.route('/save_chapter', methods=['POST'])
def save_chapter():
    etextbook_id = session.get('etextbook_id')
    # Retrieve chapter data from form
    chapter_id = request.form.get('chapter_id')
    chapter_title = request.form.get('chapter_title')
    hide_chap_id= "no"
    faculty_id = session.get('user_id')
    etextbook_list = fetch_etextbooks(etextbook_id)
    
    if etextbook_list:
        status = add_chapter_to_db(chapter_id, etextbook_id, hide_chap_id, faculty_id, chapter_title)
        if status:
            session['chap_id'] = chapter_id
            session['chap_title'] = chapter_title
            flash("Chapter saved successfully!", "success")
            return redirect(url_for('faculty.add_new_section'))   
        else:
            flash("Chapter was not saved!", "fail")
            return redirect(url_for('faculty.faculty_home'))
    else:
        flash('Textbook with Id does not exist. Please enter a new one', 'error') 

    # Redirect to the Add New Section page
    return redirect(url_for('faculty.faculty_home'))

@faculty_bp.route('/add_new_section')
def add_new_section():
    chapter_id = session.get('chap_id')
    chapter_title = session.get('chap_title')
    return render_template('add_new_section.html', chapter_id=chapter_id, chapter_title=chapter_title, call_type="new")

@faculty_bp.route('/save_section', methods=['POST'])
def save_section():
    section_id = request.form.get('section_number')
    section_title = request.form.get('section_title')

    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    faculty_id = session.get('user_id')

    hide_section_id= "no"
    chapter_list = fetch_chapters(etextbook_id, chapter_id)
    if chapter_list:
        status = add_section_to_db(section_id, chapter_id, etextbook_id, hide_section_id, faculty_id, section_title)
        if status:
            session['section_id'] = section_id
            session['section_title'] = section_title
            # Flash message to confirm the chapter was saved
            flash("Chapter saved successfully!", "success")
            return redirect(url_for('faculty.add_new_content_block', section_number=section_id))  
        else:
            flash("Chapter was not saved!", "fail")
            return redirect(url_for('faculty.faculty_home'))
    else:
        flash('Textbook with Id does not exist. Please enter a new one', 'error')

    flash("Section saved successfully!", "success")
    return redirect(url_for('faculty.faculty_home'))

@faculty_bp.route('/save_student', methods=['POST'])
def save_student():
    course_id = session.get('course_id')
    student_id = request.form.get('student_id')
    option = request.form.get('option')

    if option == '1':
        success = save_student_to_db(course_id, student_id)
        if success:
            flash("Student ID saved successfully!", "success")
        else:
            flash("Failed to save Student ID.", "error")
    return redirect(url_for('faculty.go_to_active_course'))

@faculty_bp.route('/view_worklist/<course_id>', methods=["GET", "POST"])
def view_worklist(course_id):
    waitlist = session.get('waitlist')  
    return render_template('view_worklist.html', waitlist=waitlist, courseID=course_id)

# Route for 'Change Password'
@faculty_bp.route('/faculty/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Logic to validate and update password (e.g., check current_password, then update)
        if new_password == confirm_password:
            flash("Password updated successfully", "success")
        else:
            flash("Passwords do not match", "error")
        
    return render_template('change_password.html')  # Replace with your template

# Route for 'Logout'
@faculty_bp.route('/logout')
def logout():
    session.pop('user_role', None)  # Remove user session data
    return redirect(url_for('login'))

# Dummy login route for testing
@faculty_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login logic goes here
        session['user_role'] = 'faculty'  # Mock login
        return redirect(url_for('faculty_home'))
    return render_template('login.html')