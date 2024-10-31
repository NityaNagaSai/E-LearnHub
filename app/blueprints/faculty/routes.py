from flask import Blueprint, render_template, redirect, session, url_for, request, flash
from rich import _console
from . import faculty_bp
import logging

# Configure the logging module
logging.basicConfig(level=logging.DEBUG)

@faculty_bp.route('/home', methods=['GET', 'POST'])
def faculty_home():
    return render_template('faculty_landing.html')

# Route for 'Go to Active Course'
@faculty_bp.route('/active_course')
def go_to_active_course():
    print(f"User ID") 
    print("HERE" + (url_for('faculty.view_worklist')))
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        option = request.form.get('option')
        session['course_id'] = course_id  # Save the selected course_id for later use
        
        
        if not course_id:
            flash("Please enter a valid Course ID", "error")
            return redirect(url_for('faculty.go_to_active_course'))

        # Redirect based on the selected option
        if option == '1':
            return redirect(url_for('faculty.view_worklist', course_id=course_id))
        elif option == '2':
            return redirect(url_for('faculty.approve_enrollment', course_id=course_id))
        elif option == '3':
            return redirect(url_for('faculty.view_students', course_id=course_id))
        elif option == '4':
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

@faculty_bp.route('/evaluation_course')
def go_to_evaluation_course():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        option = request.form.get('option')
        
        session['course_id'] = course_id
        
        if not course_id:
            flash("Please enter a valid Course ID", "error")
            return redirect(url_for('go_to_evaluation_course'))

        if option == '1':
            return redirect(url_for('add_chapter', course_id=course_id))
        elif option == '2':
            return redirect(url_for('modify_chapters', course_id=course_id))
        elif option == '3':
            return redirect(url_for('faculty.faculty_home'))
        else:
            flash("Invalid option selected.", "error")
            return redirect(url_for('go_to_active_course'))
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

@faculty_bp.route('/view_worklist', methods=['GET', 'POST'])
def view_worklist(courseID):
   waitlisted_students = [{"studentID" : "200535454", "name": "Emma"},
                       {"studentID" : "257303990", "name": "Daniel"} , 
                       {"studentID" : "257303980", "name": "Rupert"}]

   if request.method == 'POST':
   #Query Courses from DB and send it
   # assigned_courses = Course.query.filter_by(faculty_id=faculty_id).all()
    option = request.form.get('option')
    
    if option == '1':
        return redirect(url_for('faculty.faculty_home'))
    else:
        flash("Invalid option selected.", "error")
        return redirect(url_for('go_to_active_course'))
   return render_template('view_worklist.html', waitlist=waitlisted_students, courseID = courseID)  # Replace with your template

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