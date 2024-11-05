from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import ta_bp
from app.blueprints.ta.service import *

# TA Landing
@ta_bp.route('/home')
def ta_landing():
    return render_template('ta_landing.html')

# Go To Active Course
@ta_bp.route('/activecourse')
def active_course():
    return render_template('active_courses.html')

@ta_bp.route('/select_active_course_option', methods=['POST'])
def active_course_menu():
    course_id = request.form['course_id']
    action = request.form['action']
    
    # Redirect to the appropriate template based on the selected option
    if action == 'view_students':
        return redirect(url_for('ta.view_students', course_id = course_id))
    elif action == 'add_chapter':
        return render_template('add_chapter.html', course_id = course_id)
    elif action == 'modify_chapters':
        return render_template('modify_chapters.html', course_id = course_id)
    elif action == 'go_back':
        return render_template('ta_landing.html')  # Redirect to the user’s landing page
    
# View Courses
@ta_bp.route('/viewcourses')
def view_courses():
    user_id = session.get('user_id')
    courses = fetch_courses(user_id)
    if courses == None:
        flash("No Assigned courses!")
    return render_template('view_courses.html', courses = courses)

# Change Password
@ta_bp.route('/changepassword')
def change_password():
    return render_template('change_password.html')

@ta_bp.route('/updatepassword', methods=['POST'])
def update_password():
    user_id = session.get('user_id')  # Retrieve user_id from session
    if not user_id:
        flash("You must be logged in to change your password.", "error")
        return redirect(url_for('main.login'))

    existing_password = request.form['curr_password']
    new_password = request.form['new_password']
    confirm_new_password = request.form['confirm_new_password']
    action = request.form['action']

    if action == "update":
        if new_password != confirm_new_password:
            flash("New password and confirmation do not match.", "error")
            return redirect(url_for('ta.change_password'))

        # Verify the current password
        if not validate_current_password(user_id, existing_password):
            flash("Existing password is incorrect.", "error")
            return redirect(url_for('ta.change_password'))

        # Update the password in the database
        if update_user_password(user_id, new_password):
            flash("Password updated successfully.", "success")
            return redirect(url_for('ta.ta_landing'))
        else:
            flash("Failed to update password.", "error")
            return redirect(url_for('ta.change_password'))

    elif action == "go_back":
        return redirect(url_for('ta.ta_landing'))


# View Students
@ta_bp.route('/viewstudents/<course_id>', methods=['GET','POST'])
def view_students(course_id):
    if course_id:
        students = fetch_students(course_id)
        if students:
            return render_template('view_students.html', students=students, course_id = course_id)
        else:
            flash("No students Enrolled in this course or it's not an Active Course")
            return render_template('view_students.html', students=students , course_id = course_id)
    else:
        flash("Please enter the Course ID!")
        return render_template('view_students.html')


# Add New Chapter

# Modify Chapter

# Add New Section

# Add New Content Block

# Add Text

# Add Picture

# Add Activity

# Add Question

# Modify Section

# Modify Content Block

# Delete Content Block

# Hide Content Block

