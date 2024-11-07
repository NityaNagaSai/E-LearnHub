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
        course_list = check_course(course_id, 'Active' )
        print(course_list)
        if len(course_list) == 0:
            print("Please enter a valid Course ID", "error")
            return redirect(url_for('faculty.go_to_active_course'))

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
            return redirect(url_for('faculty.add_chapter', course_id=course_id, type='active'))
        elif option == '5':
            text_tuple = get_etextbook_id(course_id)
            etextbook_id, etextbook_title = text_tuple[0], text_tuple[1]
            session['etextbook_id'] = etextbook_id
            return redirect(url_for('faculty.modify_chapter_faculty'))
        elif option == '6':
            return redirect(url_for('faculty.create_ta'))
        elif option == '7':
            return redirect(url_for('faculty.faculty_home'))
        else:
            flash("Invalid option selected.", "error")
            return redirect(url_for('faculty.go_to_active_course'))
        
    return render_template('active_course.html')

@faculty_bp.route('/evaluation_course', methods=["GET", "POST"])
def go_to_evaluation_course():
    if request.method == 'POST':
        print("Form Data:", request.form)

        course_id = request.form.get('course_id')
        option = request.form.get('option')
        session['course_id'] = course_id  # Save the selected course_id for later use
        course_list = check_course(course_id, 'Evaluation')
        print('Inside go_to_evaluation_method:', course_id, option)

        if len(course_list) == 0:
            print("Please enter a valid Course ID", "error")
            return redirect(url_for('faculty.go_to_evaluation_course'))
        if option == '1':
            return redirect(url_for('faculty.add_chapter', course_id=course_id, type='evaluation'))
        elif option == '2':
            text_tuple = get_etextbook_id(course_id)
            etextbook_id, etextbook_title = text_tuple[0], text_tuple[1]
            session['etextbook_id'] = etextbook_id
            return redirect(url_for('faculty.modify_chapter_faculty', course_id=course_id))
        elif option == '3':
            return redirect(url_for('faculty.faculty_home'))
        else:
            flash("Invalid option selected.", "error")
            return redirect(url_for('faculty.go_to_evaluation_course'))
    return render_template('evaluation_course.html')  # Replace with your template

# Route for 'View Courses'
@faculty_bp.route('/view_courses', methods=["GET", "POST"])
def view_courses():
   user_id = session.get('user_id')
   assigned_courses = get_assigned_courses(user_id)
   print(assigned_courses)
   if len(assigned_courses) == 0:
        print("NO COURSES!", "error")
        return redirect(url_for('faculty.faculty_home'))

   if request.method == 'POST':
    option = request.form.get('option')
    
    if option == '1':
        return redirect(url_for('faculty.faculty_home'))
    else:
        flash("Invalid option selected.", "error")
        return redirect(url_for('go_to_active_course'))
   return render_template('faculty_view_courses.html', courses=assigned_courses) 

@faculty_bp.route('/view_students/<course_id>', methods=["GET", "POST"])
def view_students(course_id):
    student_list = session.get('enrolled')  
    print(student_list)
    return render_template('view_student_list.html', student_list=student_list, courseID=course_id)

@faculty_bp.route('/approve_enrollment/<course_id>' , methods=["GET", "POST"])
def approve_enrollment(course_id):
    return render_template('approve_enrollment.html', course_id = course_id)

@faculty_bp.route('/add_chapter/<course_id>')
def add_chapter(course_id):
    text_tuple = get_etextbook_id(course_id)
    etextbook_id, etextbook_title = text_tuple[0], text_tuple[1]
    course_type = request.args.get('type')
    print("Inside add_chapter:", course_type)
    session['etextbook_id'] = etextbook_id
    return render_template('faculty_add_chapter.html', etextbook_title=etextbook_title, etextbook_id=etextbook_id, call_type="new", course_type = course_type)

@faculty_bp.route('/save_chapter', methods=['POST'])
def save_chapter():
    etextbook_id = session.get('etextbook_id')
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

    return redirect(url_for('faculty.faculty_home'))

@faculty_bp.route('/add_new_section')
def add_new_section():
    chapter_id = session.get('chap_id')
    chapter_title = session.get('chap_title')
    print("Inside add new section faculty")
    return render_template('faculty_add_section.html', chapter_id=chapter_id, chapter_title=chapter_title, call_type="new")

@faculty_bp.route('/save_section', methods=['POST'])
def faculty_save_section():
    print("inside save_section_faculty")
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
            # flash("Chapter saved successfully!", "success")
            return redirect(url_for('faculty.faculty_add_new_content_block', section_number=section_id)) 
        else:
            flash("Chapter was not saved!", "fail")
            return redirect(url_for('faculty.faculty_home'))
    else:
        flash('Textbook with Id does not exist. Please enter a new one', 'error')


    # flash("Section saved successfully!", "success")
    return redirect(url_for('faculty.faculty_home'))

@faculty_bp.route('/add_new_content_block')
def faculty_add_new_content_block():
   section_number = session.get('section_number')
   section_title = session.get('section_title')
   return render_template('faculty_add_new_content_block.html',section_number=section_number, section_title=section_title, call_type="new")

@faculty_bp.route('/save_content_block', methods=['POST'])
def faculty_save_content_block():
   content_block_id = request.form.get('content_block_id')
   session['content_block_id'] = content_block_id  # Store content_block_id in session
   action = request.form.get('action')
   if action == 'add_text':
       return redirect(url_for('faculty.faculty_add_text', call_type="new"))
   elif action == 'add_picture':
       return redirect(url_for('faculty.faculty_add_picture', call_type="new"))
   elif action == 'add_activity':
       return redirect(url_for('faculty.faculty_add_activity'))
   else:
       flash("Invalid action selected", "error")
       return redirect(url_for('faculty.faculty_add_new_content_block'))


@faculty_bp.route('/add_text')
def faculty_add_text():
   call_type = request.args.get('call_type')
   content_block_id = session.get('content_block_id')
   return render_template('faculty_add_text.html', content_block_id=content_block_id, call_type = call_type)


@faculty_bp.route('/add_picture')
def faculty_add_picture():
   call_type = request.args.get('call_type')
   content_block_id = session.get('content_block_id')
   return render_template('faculty_add_picture.html', content_block_id=content_block_id, call_type = call_type)


@faculty_bp.route('/add_activity')
def faculty_add_activity():
   call_type = request.args.get('call_type')
   content_block_id = session.get('content_block_id')
   return render_template('faculty_add_activity.html', content_block_id=content_block_id)


@faculty_bp.route('/save_text', methods=['POST'])
def faculty_save_text():
   text = request.form.get('text')
   # Save the text content block (you would save it in the database)
   flash("Text added successfully!", "success")
   section_id = session.get('section_id')
   content_block_id = session.get('content_block_id')
   etextbook_id = session.get('etextbook_id')
   chapter_id = session.get('chap_id')
   admin_id = session.get('user_id')
   is_hidden= "no"
   content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
   if content_block_list:
       delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
       if delete_status:
           status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'text', text)
           if status:
               flash("Text saved successfully!", "success")
               return redirect(url_for('faculty.faculty_add_new_content_block')) 
           else:
               flash("Text was not saved!", "fail")
               return redirect(url_for('faculty.faculty_add_new_content_block'))
       else:
           flash("Text was not saved!", "fail")
           return redirect(url_for('faculty.faculty_add_new_content_block'))
   else:
       status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'text', text)
       if status:
           flash("Text saved successfully!", "success")
           return redirect(url_for('faculty.faculty_add_new_content_block')) 
       else:
           flash("Text was not saved!", "fail")
           return redirect(url_for('faculty.faculty_add_new_content_block'))


@faculty_bp.route('/save_picture', methods=['POST'])
def faculty_save_picture():
   picture_url = request.form.get('picture')
   #request.form.get('picture')
   # Save the picture content block
   # flash("Text added successfully!", "success")
   section_id = session.get('section_id')
   content_block_id = session.get('content_block_id')
   etextbook_id = session.get('etextbook_id')
   chapter_id = session.get('chap_id')
   admin_id = session.get('user_id')
   is_hidden= "no"
   content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
   print("Inside save_picture method:", content_block_list)
   if content_block_list:
       delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
       print(delete_status)
       if delete_status:
           status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'image', picture_url)
           if status:
               flash("Picture saved successfully!", "success")
               return redirect(url_for('faculty.faculty_add_new_content_block')) 
           else:
               flash("Picture was not saved!", "fail")
               return redirect(url_for('faculty.faculty_add_new_content_block'))
       else:
           flash("Picture was not saved!", "fail")
           return redirect(url_for('faculty.faculty_add_new_content_block'))
   else:
       status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'image', picture_url)
       if status:
           flash("Picture saved successfully!", "success")
           return redirect(url_for('faculty.faculty_add_new_content_block')) 
       else:
           flash("Picture was not saved!", "fail")
           return redirect(url_for('faculty.faculty_add_new_content_block'))


@faculty_bp.route('/save_activity', methods=['POST'])
def faculty_save_activity():
   activity_id = request.form.get('activity_id')
   session['activity_id'] = activity_id  # Store activity ID in session for adding questions
   section_id = session.get('section_id')
   content_block_id = session.get('content_block_id')
   etextbook_id = session.get('etextbook_id')
   chapter_id = session.get('chap_id')
   admin_id = session.get('user_id')


   print("inside save_activity method:",etextbook_id)
   content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
   if content_block_list:
       content_type = content_block_list[0][4]
       if content_type == 'activity':
           activity_data = fetch_activity(etextbook_id, chapter_id, section_id, content_block_id, activity_id)
           if activity_data:
               return redirect(url_for('faculty.faculty_add_question'))
           else:
               status = add_activity_to_db(etextbook_id, chapter_id, section_id, content_block_id,
                                           activity_id, "no", admin_id)
               if status:
                   return redirect(url_for('faculty.faculty_add_question'))
               else:
                   flash("Error in saving the activity. Please try again.", "error")
                   return redirect(url_for('faculty.faculty_add_activity'))  
       else:
           delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
           if delete_status:
               status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, 'no', admin_id, 'activity', activity_id)
               if status:
                   return redirect(url_for('faculty.faculty_add_question'))
               else:
                   flash("Error in saving the activity. Please try again.", "error")
                   return redirect(url_for('faculty.faculty_add_activity'))  
           else:
               flash("Error in saving the activity. Please try again.", "error")
               return redirect(url_for('faculty.faculty_add_new_content_block'))        
   else:
       if add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, 'no', admin_id, 'activity', activity_id):
           status = add_activity_to_db(etextbook_id, chapter_id, section_id, content_block_id,
                                           activity_id, "no", admin_id)
           if status:
               return redirect(url_for('faculty.faculty_add_question'))
           else:
               flash("Error in saving the activity. Please try again.", "error")
               return redirect(url_for('faculty.faculty_add_activity'))
       else:
           flash("Error in saving the Block. Please try again.", "error")
           return redirect(url_for('faculty.faculty_add_activity'))


@faculty_bp.route('/add_question')
def faculty_add_question():
   activity_id = session.get('activity_id')
   return render_template('faculty_add_question.html', activity_id=activity_id)


@faculty_bp.route('/save_question', methods=['POST'])
def faculty_save_question():


   section_id = session.get('section_id')
   content_block_id = session.get('content_block_id')
   etextbook_id = session.get('etextbook_id')
   chapter_id = session.get('chap_id')
   activity_id = session.get('activity_id')
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
       return redirect(url_for('faculty.faculty_add_question'))
   else:
       status = add_activity_question(question_id, activity_id, content_block_id, etextbook_id, section_id, chapter_id,
                                      question_text, correct_answer, option1_text, option2_text, option3_text, option4_text,
                                      option1_explanation, option2_explanation, option3_explanation, option4_explanation)
       if status:
           # Flash a success message and redirect to Add Activity page
           flash("Question added successfully!", "success")
           return redirect(url_for('faculty.faculty_add_activity'))
       else:
           flash("Error in adding the question", "error")
           return redirect(url_for('faculty.faculty_add_question'))

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
@faculty_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    return render_template('faculty_change_password.html')  # Replace with your template

# Route for 'Logout'
@faculty_bp.route('/logout')
def logout():
    print("Inside logout method")
    session.clear()
    return redirect(url_for('main.index'))

# Dummy login route for testing
@faculty_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login logic goes here
        session['user_role'] = 'faculty'  # Mock login
        return redirect(url_for('faculty_home'))
    return render_template('login.html')

@faculty_bp.route('/create_ta', methods=["GET", "POST"])
def create_ta():
    if request.method == "GET":
        return render_template('create_ta.html')
    elif request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        course_id = session.get('course_id')
        user_id = create_new_ta(first_name, last_name, email, password)
        if user_id:
            course_status = add_ta_to_course(user_id,course_id)
            if course_status: 
                flash('New TA account created successfully!', 'success')
        else:
            flash('An error occured in creating the account', 'error')
        return redirect(url_for('admin.admin_landing')) 

@faculty_bp.route('/update_password', methods=['POST'])
def update_password_faculty():
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
            return redirect(url_for('faculty.change_password'))

        # Verify the current password
        if not validate_current_password(user_id, existing_password):
            flash("Existing password is incorrect.", "error")
            return redirect(url_for('faculty.change_password'))

        # Update the password in the database
        if update_user_password(user_id, new_password):
            flash("Password updated successfully.", "success")
            return redirect(url_for('faculty.faculty_home'))
        else:
            flash("Failed to update password.", "error")
            return redirect(url_for('faculty.change_password'))

    elif action == "go_back":
        return redirect(url_for('faculty.faculty_home'))
    
@faculty_bp.route('/modify_chapter', methods=['GET','POST'])
def modify_chapter_faculty():
    if request.method == 'POST':
        etextbook_id = session['etextbook_id']
        chapter_id = request.form.get('chapter_id')
        session['chap_id'] = chapter_id
        action = request.form.get('action')

        # Logic to modify the chapter in the specified E-textbook in the database
        chapter_list = fetch_chapters(etextbook_id, chapter_id)
        if chapter_list:
            if action == "add_new_section":
                return redirect(url_for('faculty.add_new_section'))
            elif action == "modify_section":
                return redirect(url_for('faculty.modify_section_faculty'))
            elif action == "hide_chapter":
                if modify_chapter_hidden(chapter_id, etextbook_id):
                    flash("Chapter is now hidden", "success")
                    return redirect(url_for('faculty.faculty_home'))
            elif action == "delete":
                if delete_chapter(chapter_id, etextbook_id):
                    flash("Chapter is now deleted", "success")
                    return redirect(url_for('faculty.faculty_home'))
        else:
            flash("No chapter exists with the current chapter id. Please try again.", "error")

        return redirect(url_for('faculty.modify_chapter_faculty'))

    return render_template('faculty_modify_chapter.html')

@faculty_bp.route('/modify_section_faculty', methods=['GET', 'POST'])
def modify_section_faculty():
    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    if request.method == 'POST':
        print("Inside modify section method")
        section_number = request.form.get('section_number')
        session['section_id'] = section_number
        action = request.form.get("action")
        print(etextbook_id, chapter_id, section_number)
        sections_list = fetch_sections(etextbook_id, chapter_id, section_number)
        if sections_list:
            if action == "add_new_content_block":
                return redirect(url_for("faculty.faculty_add_new_content_block"))
            elif action == "modify_content_block":
                return redirect(url_for("faculty.modify_content_block_faculty"))
            elif action == "hide":
                if modify_section_hidden(chapter_id, etextbook_id, section_number):
                    flash("Section is now hidden", "success")
                    return redirect(url_for('faculty.faculty_home'))
            elif action == "delete":
                if delete_section(chapter_id, etextbook_id, section_number):
                    flash("Section is now deleted", "success")
                    return redirect(url_for('faculty.faculty_home'))
        else:
            flash(f"Section number {section_number} does not exist. Please try again", "error")
        # return redirect(url_for('admin.modify_content_block'))
    return render_template('faculty_modify_section.html', etextbook_id = etextbook_id, chapter_id=chapter_id)

@faculty_bp.route('/modify_content_block_faculty', methods=['GET', 'POST'])
def modify_content_block_faculty():
    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    section_id= session.get('section_id')
    if request.method == 'POST':
        content_block_id = request.form.get('content_block_id')
        session['content_block_id'] = content_block_id  # Store content_block_id in session

        action = request.form.get('action')
        if action == 'modify_text':
            return redirect(url_for('faculty.faculty_add_text', call_type="modify"))
        elif action == 'modify_picture':
            return redirect(url_for('faculty.faculty_add_picture', call_type="modify"))
        elif action == 'modify_activity':
            return redirect(url_for('faculty.faculty_add_activity', call_type="modify"))
        elif action == "hide":
                if modify_content_block_hidden(chapter_id, etextbook_id, section_id, content_block_id):
                    flash("Content is now hidden", "success")
                    return redirect(url_for('faculty.faculty_home'))
        elif action == "delete":
                if delete_content_block(chapter_id, etextbook_id, section_id,content_block_id ):
                    flash("Content is now deleted", "success")
                    return redirect(url_for('faculty.faculty_home'))
        elif action == "hide_activity":
             return redirect(url_for('faculty.hide_activity', call_type="modify"))
        elif action == "delete_activity":
             return redirect(url_for('faculty.delete_activity', call_type="modify"))
        else:
            flash("Invalid action selected", "error")
            return redirect(url_for('faculty.modify_content_block_faculty'))
    return render_template('faculty_modify_content_block.html')

@faculty_bp.route('/hide_activity')
def hide_activity():
    etextbook_id = session.get('etextbook_id')
    return render_template('hide_activity.html', etextbook_id=etextbook_id)

@faculty_bp.route('/hide_activity_action', methods=['POST'])
def hide_activity_action():
    etextbook_id = session.get('etextbook_id')
    chapter_id = request.form.get('chapter_id')
    chapter_id = session.get('chap_id')
    section_id= session.get('section_id')
    content_block_id = session.get('content_block_id')
    activity_id = request.form.get('activity_id')
    status = modify_activity_hidden(chapter_id, etextbook_id, section_id,content_block_id,activity_id )
    if status:
        flash("Activity hiddem successfully!", "success")
        return redirect(url_for('faculty.faculty_home'))   
    else:
        flash("Activity Not Hidden", "fail")
        return redirect(url_for('faculty.modify_content_block_faculty'))


@faculty_bp.route('/delete_activity')
def delete_activity():
    etextbook_id = session.get('etextbook_id')
    return render_template('delete_activity.html', etextbook_id=etextbook_id)

@faculty_bp.route('/delete_activity_action', methods=['POST'])
def delete_activity_action():
    etextbook_id = session.get('etextbook_id')
    chapter_id = request.form.get('chapter_id')
    chapter_id = session.get('chap_id')
    section_id= session.get('section_id')
    content_block_id = session.get('content_block_id')
    activity_id = request.form.get('activity_id')
    status = modify_delete_activity(chapter_id, etextbook_id, section_id,content_block_id,activity_id)
    if status:
        flash("Activity deteted successfully!", "success")
        return redirect(url_for('faculty.faculty_home'))   
    else:
        flash("Activity was not deleted!", "fail")
        return redirect(url_for('faculty.modify_content_block_faculty'))