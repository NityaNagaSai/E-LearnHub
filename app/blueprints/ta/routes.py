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
    session["course_id"] = course_id
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
@ta_bp.route('/view_students/<course_id>', methods=['GET','POST'])
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
    action = request.form['action']
    # Validate that the course exists and is active
    course = check_active_course(course_id)

    if course:
        # Access elements in course tuple by index
        session['course_id'] = course[0]  # course_id
        session['textbook_id'] = course[2]  # textbook_id
        # Redirect to the appropriate template based on the selected option
        if action == 'view_students':
            return redirect(url_for('ta.view_students', course_id = course_id))
        elif action == 'add_chapter':
            return redirect(url_for('ta.add_chapter_form'))
        elif action == 'modify_chapters':
            return redirect(url_for('ta.ta_modify_chapter'))
        elif action == 'go_back':
            return render_template('ta_landing.html')  # Redirect to the user’s landing page
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
        return redirect(url_for('ta.add_new_section2', chapter_id=chapter_id, textbook_id=textbook_id))

    return render_template('add_chapter.html')


@ta_bp.route('/add_new_section2')
def add_new_section2():
    chapter_id = request.args.get('chapter_id')
    textbook_id = request.args.get('textbook_id')  
    print(f"chapter_id: {chapter_id}")
    print(f"textbook_id: {textbook_id}")

    return render_template('add_new_section2.html', chapter_id=chapter_id, textbook_id=textbook_id)

@ta_bp.route('/save_section2', methods=['POST'])
def save_section2():
    # Retrieve form data
    section_id = request.form.get('section_number')
    section_title = request.form.get('section_title')

    # Retrieve necessary data from the session
    chapter_id = session.get('chapter_id')
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
            session['etextbook_id'] = textbook_id  # Ensure this is saved for later use
            session['chap_id'] = chapter_id 

            # Flash a success message and redirect to add a content block
            flash("Section added successfully!", "success")
            print(f"This block : 1")
            return redirect(url_for('ta.add_new_content_block2',chapter_id=chapter_id, section_number=section_id))
        else:
            flash("Failed to add section. Please try again.", "error")
            print(f"This block : 2")
            return redirect(url_for('ta.add_new_section2'))
    else:
        flash("The specified chapter does not exist. Please enter a valid chapter ID.", "error")
        print(f"This block : 3")
        return redirect(url_for('ta.add_new_section2'))
    
@ta_bp.route('/add_new_content_block2')
def add_new_content_block2():
    section_number = session.get('section_number')
    section_title = session.get('section_title')
    chapter_id = request.args.get('chapter_id')
    return render_template('add_new_content_block2.html',chapter_id=chapter_id,section_number=section_number, section_title=section_title)


@ta_bp.route('/save_content_block2', methods=['POST'])
def save_content_block2():
    content_block_id = request.form.get('content_block_id')
    chapter_id = request.form.get('chapter_id')
    session['content_block_id'] = content_block_id
    action = request.form.get('action')
    if action == 'add_text':
        return redirect(url_for('ta.add_text2',chapter_id=chapter_id))
    elif action == 'add_picture':
        return redirect(url_for('ta.add_picture2',chapter_id=chapter_id))
    elif action == 'add_activity':
        return redirect(url_for('ta.add_activity2',chapter_id=chapter_id))
    else:
        flash("Invalid action selected", "error")
        return redirect(url_for('ta.add_new_content_block2',chapter_id=chapter_id))
    

@ta_bp.route('/add_text2')
def add_text2():
    chapter_id = request.args.get('chapter_id')
    content_block_id = session.get('content_block_id')
    
    return render_template('add_text2.html', content_block_id=content_block_id,chapter_id=chapter_id)

@ta_bp.route('/add_picture2')
def add_picture2():
    chapter_id = request.args.get('chapter_id')
    content_block_id = session.get('content_block_id')
    return render_template('add_picture2.html', content_block_id=content_block_id,chapter_id=chapter_id)

@ta_bp.route('/add_activity2')
def add_activity2():
    content_block_id = session.get('content_block_id')
    chapter_id = request.args.get('chapter_id')
    return render_template('add_activity2.html', content_block_id=content_block_id,chapter_id=chapter_id)

@ta_bp.route('/save_text2', methods=['POST'])
def save_text2():
    text = request.form.get('text')
    flash("Text added successfully!", "success")
    section_id = session.get('section_id')
    content_block_id = session.get('content_block_id')
    etextbook_id = session.get('textbook_id')
    chapter_id = request.form.get('chapter_id')
    admin_id = session.get('user_id')
    is_hidden= "no"
    content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
    if content_block_list:
        delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
        if delete_status:
            status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'text', text)
            if status:
                flash("Text saved successfully!", "success")
                return redirect(url_for('ta.add_new_section2'))  
            else:
                flash("Text was not saved!", "fail")
                return redirect(url_for('ta.add_new_content_block2'))
        else:
            flash("Text was not saved!", "fail")
            return redirect(url_for('ta.add_new_content_block2'))
    else:
        status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'text', text)
        if status:
            flash("Text saved successfully!", "success")
            return redirect(url_for('ta.add_new_section2'))  
        else:
            flash("Text was not saved!", "fail")
            return redirect(url_for('ta.add_new_content_block2'))

# Modify Chapter

@ta_bp.route('/modify_chapter', methods=['GET','POST'])
def ta_modify_chapter():
    if request.method == 'POST':
        course_id = session.get("course_id")
        course = check_active_course(course_id)
        session['textbook_id'] = course[2]
        # etextbook_id = session.get('etextbook_id')
        chapter_id = request.form.get('chapter_id')
        session['chapter_id'] = chapter_id
        textbook_id = session.get('textbook_id')
        course_id = session.get('course_id')
        print(textbook_id, chapter_id)
        action = request.form.get('action')
        # Logic to modify the chapter in the specified E-textbook in the database
        chapter_list = fetch_chapters(textbook_id, chapter_id)
        print(chapter_list)
        if chapter_list:
            if action == "add_new_section":
                return redirect(url_for('ta.add_new_section2'))
            elif action == "modify_section":
                return redirect(url_for('ta.ta_modify_section'))
        else:
            flash("No chapter exists with the current chapter id or TA is not assigned to this course/chapter. Please try again.", "error")
            # # flash(f"Chapter modified for E-textbook ID {etextbook_id}.", "success")
            return redirect(url_for('ta.ta_modify_chapter'))

    return render_template('ta_modify_chapter.html')


# Modify Section

@ta_bp.route('/modify_section', methods=['GET', 'POST'])
def ta_modify_section():
    # if request.method == "GET":
    etextbook_id = session.get('textbook_id')
    chapter_id = session.get('chapter_id')
    course_id = session.get('course_id')
    if request.method == 'POST':
        print("Inside modify section method")
        section_number = request.form.get('section_number')
        session['section_number'] = section_number
        action = request.form.get("action")
        sections_list = fetch_sections(etextbook_id, chapter_id, section_number)
        if sections_list:
            if action == "add_new_content_block":
                return redirect(url_for("ta.add_new_content_block2"))
            elif action == "modify_content_block":
                return redirect(url_for("ta.ta_modify_content_block"))
            elif action == "delete_content_block":
                return redirect(url_for("ta.ta_delete_content_block"))
            elif action == "hide_content_block":
                return redirect(url_for("ta.ta_hide_content_block"))
        else:
            flash(f"Section number {section_number} does not exist. Please try again", "error")
            return redirect(url_for('ta.ta_modify_section'))
    return render_template('ta_modify_section.html', etextbook_id = etextbook_id, chapter_id=chapter_id)

# Modify Content Block
@ta_bp.route('/modify_content_block', methods=['GET', 'POST'])
def ta_modify_content_block():
    if request.method == 'POST':
        content_block_id = request.form.get('content_block_id')
        session['content_block_id'] = content_block_id  # Store content_block_id in session

        action = request.form.get('action')
        if action == 'add_text':
            return redirect(url_for('ta.add_text2', call_type="modify"))
        elif action == 'add_picture':
            return redirect(url_for('ta.add_picture2', call_type="modify"))
        elif action == 'modify_activity':
            return redirect(url_for('ta.add_activity2'))
        else:
            flash("Invalid action selected", "error")
            return redirect(url_for('ta.ta_modify_content_block'))
    return render_template('ta_modify_content_block.html')

# Delete Content Block
@ta_bp.route('/delete_content_block', methods=['GET', 'POST'])
def ta_delete_content_block():
    if request.method == 'POST':
        content_block_id = request.form.get('content_block_id')
        session['content_block_id'] = content_block_id  # Store content_block_id in session
        course_id = session.get('course_id')
        textbook_id = session.get('textbook_id')
        chapter_id = session.get('chapter_id')
        section_id = session.get('section_number')
        action = request.form.get('action')
        print(textbook_id, chapter_id, section_id, content_block_id)
        if action == 'delete_block':
            # method to delete the block from db table
            result = delete_content(textbook_id, chapter_id, section_id, content_block_id)
            if result:
                flash("Content Block successfully deleted", "success")
            else:
                flash(f"There is no {content_block_id} in the Contents", "error")
        else:
            flash("Invalid action selected", "error")
        return redirect(url_for('ta.ta_delete_content_block'))
    return render_template('ta_delete_content_block.html')
# Hide Content Block



@ta_bp.route('/save_picture2', methods=['POST'])
def save_picture2():
    picture_url = "sample1.png"
    #request.form.get('picture')
    # Save the picture content block
    flash("Text added successfully!", "success")
    section_id = session.get('section_id')
    content_block_id = session.get('content_block_id')
    etextbook_id = session.get('textbook_id')
    chapter_id = session.get('chap_id')
    admin_id = session.get('user_id')
    print(f"Section ID: {section_id}")
    print(f"Content Block ID: {content_block_id}")
    print(f"eTextbook ID: {etextbook_id}")
    print(f"Chapter ID: {chapter_id}")
    print(f"Admin ID: {admin_id}")
    is_hidden= "no"
    content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
    if content_block_list:
        delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
        if delete_status:
            status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'image', picture_url)
            if status:
                flash("Picture saved successfully!", "success")
                return redirect(url_for('ta.add_new_content_block2'))  
            else:
                flash("Picture was not saved!", "fail")
                return redirect(url_for('ta.add_new_content_block2'))
        else:
            flash("Picture was not saved!", "fail")
            return redirect(url_for('ta.add_new_content_block2'))
    else:
        status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'image', picture_url)
        if status:
            flash("Picture saved successfully!", "success")
            return redirect(url_for('ta.add_new_content_block2'))  
        else:
            flash("Picture was not saved!", "fail")
            return redirect(url_for('ta.add_new_content_block2'))



@ta_bp.route('/save_activity2', methods=['POST'])
def save_activity2():
    activity_id = request.form.get('activity_id')
    session['activity_id'] = activity_id  # Store activity ID in session for adding questions
    section_id = session.get('section_id')
    content_block_id = session.get('content_block_id')
    etextbook_id = session.get('textbook_id')
    chapter_id = session.get('chap_id')
    admin_id = session.get('user_id')

    print("inside save_activity method:",etextbook_id)
    activity_data = fetch_activity(etextbook_id, chapter_id, section_id, content_block_id, activity_id)
    if activity_data:
        return redirect(url_for('ta.add_question2'))

        # flash("Activity with the entered ID already exists. Please enter a unique ID", "error")
        # return redirect(url_for('admin.add_activity'))
    else:
        if add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, 'no', admin_id, 'activity', activity_id):
            status = add_activity_to_db(etextbook_id, chapter_id, section_id, content_block_id, 
                                            activity_id, "no", admin_id)
            if status:
                return redirect(url_for('ta.add_question2',chapter_id=chapter_id))
            else:
                flash("Error in saving the activity. Please try again.", "error")
                return redirect(url_for('ta.add_activity2'))
        else:
            flash("Error in saving the Block. Please try again.", "error")
            return redirect(url_for('ta.add_activity2'))

@ta_bp.route('/add_question2')
def add_question2():
    activity_id = session.get('activity_id') 
    chapter_id = request.args.get('chapter_id')
    return render_template('add_question2.html', activity_id=activity_id,chapter_id=chapter_id)

@ta_bp.route('/save_question2', methods=['POST'])
def save_question2():

    section_id = session.get('section_id')
    content_block_id = session.get('content_block_id')
    etextbook_id = session.get('textbook_id')
    chapter_id = request.form.get('chapter_id')
    activity_id = session.get('activity_id')
    print(f"Section ID: {section_id}")
    print(f"Content Block ID: {content_block_id}")
    print(f"eTextbook ID: {etextbook_id}")
    print(f"Chapter ID: {chapter_id}")
    print("Inside save_question method:", etextbook_id)
    # Retrieve question and option details from the form
    question_id = request.form.get('question_id')
    question_text = request.form.get('question_text')
    correct_answer = request.form.get('answer_key')
    
    # Option 1
    option1_text = request.form.get('option1_text')
    option1_explanation = request.form.get('option1_explanation')
    # option1_label = request.form.get('option1_label')

    # Option 2
    option2_text = request.form.get('option2_text')
    option2_explanation = request.form.get('option2_explanation')
    # option2_label = request.form.get('option2_label')

    # Option 3
    option3_text = request.form.get('option3_text')
    option3_explanation = request.form.get('option3_explanation')
    # option3_label = request.form.get('option3_label')

    # Option 4
    option4_text = request.form.get('option4_text')
    option4_explanation = request.form.get('option4_explanation')
    # option4_label = request.form.get('option4_label')

    # if option1_label == "Correct":
    #     correct_answer = 1
    # elif option2_label == "Correct":
    #     correct_answer = 2
    # elif option3_label == "Correct":
    #     correct_answer = 3
    # else:
    #     correct_answer = 4

    # Here you would save the question and options to the database
    questions_list = fetch_activity_questions(etextbook_id, chapter_id, section_id, content_block_id, activity_id, question_id)
    if questions_list:
        flash("Question with same ID exists. Please enter a unique ID", "error")
        return redirect(url_for('ta.add_question'))
    else:
        status = add_activity_question(question_id, activity_id, content_block_id, etextbook_id, section_id, chapter_id,
                                       question_text, correct_answer, option1_text, option2_text, option3_text, option4_text,
                                       option1_explanation, option2_explanation, option3_explanation, option4_explanation)
        if status:
            # Flash a success message and redirect to Add Activity page
            flash("Question added successfully!", "success")
            return redirect(url_for('ta.add_activity2'))
        else:
            flash("Error in adding the question", "error")
            return redirect(url_for('ta.add_question2'))


