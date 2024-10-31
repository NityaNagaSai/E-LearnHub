from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import ta_bp

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
        return render_template('view_students.html', course_id=course_id)
    elif action == 'add_chapter':
        return render_template('add_chapter.html', course_id=course_id)
    elif action == 'modify_chapters':
        return render_template('modify_chapters.html', course_id=course_id)
    elif action == 'go_back':
        return render_template('ta_landing.html')  # Redirect to the user’s landing page
    
# View Courses
@ta_bp.route('/viewcourses')
def view_courses():
    return render_template('view_courses.html')

# Change Password
@ta_bp.route('/changepassword')
def change_password():
    return render_template('change_password.html')

@ta_bp.route('/updatepassword', methods=['POST'])
def update_password():
    existing_password = request.form['curr_password']
    new_password = request.form['new_password']
    confirm_new_password = request.form['confirm_new_password']
    action = request.form['action']
    if action == "update":
        if new_password != confirm_new_password:
        # flash("New password and confirmation do not match.", "error")
            return redirect(url_for('update_password'))

    if new_password == confirm_new_password:
        # write logic to update the password in the database
        # flash("Password updated successfully.", "success")
        return render_template('ta_landing.html')  # Replace with the actual previous page

    elif action == "go_back":
        return render_template('ta_landing.html')

# View Students

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

