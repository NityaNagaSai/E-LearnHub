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
    

@ta_bp.route('/verify_course', methods=['POST'])
def verify_course():
    # Get the course_id from the form
    course_id = request.form.get('course_id')

    # Validate that the course exists and is active
    course = check_active_course(course_id)

    if course:
        # Access elements in course tuple by index
        session['course_id'] = course[0]  # course_id
        session['textbook_id'] = course[2]  # textbook_id
        return redirect(url_for('ta.add_chapter_form'))
    else:
        # Flash an error message and redirect back to the active courses page
        flash("Course ID is invalid or the course is not active.")
        return redirect(url_for('ta.active_course'))
    

@ta_bp.route('/add_chapter', methods=['GET', 'POST'])
def add_chapter():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        
        # Validate course_id and check if course is active
        course = check_active_course(course_id)
        
        if not course:
            flash("Course ID is invalid or the course is not active.")
            return redirect(url_for('ta.active_course'))  # Redirect back to active courses page if invalid

        # Save course_id in session for future use (like in add_chapter.html)
        session['course_id'] = course_id
        session['textbook_id'] = course['textbook_id']  # Save textbook_id to use in chapter creation
        
        # Redirect to add_chapter.html with necessary course information
        return redirect(url_for('ta.add_chapter_form'))

    return redirect(url_for('ta.active_course'))

@ta_bp.route('/add_chapter_form', methods=['GET', 'POST'])
def add_chapter_form():
    if request.method == 'POST':
        action = request.form.get('action')

        # If 'Go Back' button is clicked, redirect to active course menu
        if action == 'go_back':
            return redirect(url_for('ta.active_course_menu'))
        
        # Proceed with adding the chapter if 'Add Chapter' is clicked
        chapter_id = request.form.get('chapter_id')
        chapter_title = request.form.get('chapter_title')
        is_hidden = "no"
        created_by = session.get('user_id')
        textbook_id = session.get('textbook_id')
        course_id = session.get('course_id')  # Retrieve course_id from session
        print(f"chapter_id: {chapter_id}")
        print(f"chapter_title: {chapter_title}")
        print(f"is_hidden: {is_hidden}")
        print(f"created_by (user_id): {created_by}")
        print(f"textbook_id: {textbook_id}")
        print(f"course_id: {course_id}")

        # Call the updated add_chapter function with correct arguments
        success = add_chapter_to_db(chapter_id, textbook_id, is_hidden, created_by, chapter_title)
        
        message = "Chapter added successfully!" if success else "Failed to add chapter."
        flash(message)

        # Pass course_id and textbook_id as query parameters to add_section route
        return redirect(url_for('ta.add_new_section', chapter_id=chapter_id, textbook_id=textbook_id))

    return render_template('add_chapter.html')


@ta_bp.route('/add_new_section')
def add_new_section():
    chapter_id = request.args.get('chapter_id')
    textbook_id = request.args.get('textbook_id')  
    print(f"chapter_id: {chapter_id}")
    print(f"textbook_id: {textbook_id}")

    return render_template('add_new_section.html', chapter_id=chapter_id, textbook_id=textbook_id)

# Route to save the section details after form submission
@ta_bp.route('/save_section', methods=['POST'])
def save_section():
    # Retrieve form data
    section_id = request.form.get('section_number')
    section_title = request.form.get('section_title')

    # Retrieve necessary data from the session
    chapter_id = request.form.get('chapter_id')
    textbook_id = session.get('textbook_id')
    
    user_id = session.get('user_id')
    is_hidden = "no"  # Default visibility setting
    print(f"chapter_id: {chapter_id}")
    print(f"textbook_id: {textbook_id}")

    # Fetch chapters to validate the existence of the chapter
    chapter_list = fetch_chapters(textbook_id, chapter_id)
    if chapter_list:
        # If the chapter exists, proceed to save the section
        status = add_section_to_db(section_id, chapter_id, textbook_id, is_hidden, user_id, section_title)
        if status:
            # Save section details in session for future use
            session['section_id'] = section_id
            session['section_title'] = section_title

            # Flash a success message and redirect to add a content block
            flash("Section added successfully!", "success")
            print(f"This block : 1")
            return redirect(url_for('admin.add_new_content_block', section_number=section_id))
        else:
            flash("Failed to add section. Please try again.", "error")
            print(f"This block : 2")
            return redirect(url_for('admin.add_new_section'))
    else:
        flash("The specified chapter does not exist. Please enter a valid chapter ID.", "error")
        print(f"This block : 3")
        return redirect(url_for('admin.add_new_section'))




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

