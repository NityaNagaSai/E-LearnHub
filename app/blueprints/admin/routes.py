from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from . import admin_bp
import mysql.connector
from mysql.connector import errorcode
from app.blueprints.admin.service import create_new_faculty_account, add_etextbook_to_db, fetch_etextbooks


@admin_bp.route('/home')
def admin_landing():
    return render_template('admin_landing.html')

@admin_bp.route('/create_faculty', methods=["GET", "POST"])
def create_faculty():
    if request.method == "GET":
        return render_template('create_faculty.html')
    elif request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        action = request.form['action']
        
        if action == 'create_faculty_user':
            status = create_new_faculty_account(first_name, last_name, email, password)
            if status:
                flash('New Faculty account created successfully!', 'success')
            else:
                flash('An error occured in creating the account', 'error')
            return redirect(url_for('admin.admin_landing')) 

        elif action == 'go_back':
            return render_template('admin_landing.html') 

@admin_bp.route('/createetextbook')
def create_etextbook():
    return render_template('create_etextbook.html')

@admin_bp.route('/add_etextbook', methods=['POST'])
def add_etextbook():
    # Get form data
    title = request.form.get('title')
    etextbook_id = request.form.get('etextbook_id')
    etextbook_list = fetch_etextbooks(etextbook_id)
    session['etextbook_title'] = title
    session['etextbook_id'] = etextbook_id
    if etextbook_list:
        # display a message showing textbook with same id exists and ask them to change the textbook id
         flash('Textbook with Id exists. Please enter a new one', 'error')
    else:
        status = add_etextbook_to_db(etextbook_id, title)
        if status:
            # write code to display message
            # Redirect to the Add New Chapter page
             # Store data in the session (or save to database as needed)
            session['etextbook_title'] = title
            session['etextbook_id'] = etextbook_id
            return redirect(url_for('admin.new_chapter'))
        else:
            return redirect(url_for('admin.admin_landing')) 
    

@admin_bp.route('/createetextbook/newchapter')
def new_chapter():
    etextbook_title = session.get('etextbook_title')
    etextbook_id = session.get('etextbook_id')
    return render_template('new_chapter.html', etextbook_title=etextbook_title, etextbook_id=etextbook_id)


@admin_bp.route('/save_chapter', methods=['POST'])
def save_chapter():
    etextbook_id = session.get('etextbook_id')
    # Retrieve chapter data from form
    chapter_id = request.form.get('chapter_id')
    chapter_title = request.form.get('chapter_title')
    hide_chap_id= "no"
    admin_id = session.get('user_id')
    etextbook_list = fetch_etextbooks(etextbook_id)
    
    if etextbook_list:
        status = add_chapter_to_db(chapter_id, etextbook_id, hide_chap_id, admin_id, chapter_title)
        if status:
            session['chap_id'] = chapter_id
            session['chap_title'] = chapter_title
            # Flash message to confirm the chapter was saved
            flash("Chapter saved successfully!", "success")
            return redirect(url_for('admin.add_new_section'))   
        else:
            flash("Chapter was not saved!", "fail")
            return redirect(url_for('admin.admin_landing'))
    else:
        flash('Textbook with Id does not exist. Please enter a new one', 'error') 

    # Redirect to the Add New Section page
    return redirect(url_for('admin.admin_landing'))


@admin_bp.route('/add_new_section')
def add_new_section():
    chapter_id = session.get('chapter_id')
    chapter_title = session.get('chapter_title')
    return render_template('add_new_section.html', chapter_id=chapter_id, chapter_title=chapter_title)

@admin_bp.route('/save_section', methods=['POST'])
def save_section():
    section_number = request.form.get('section_number')
    section_title = request.form.get('section_title')

    etextbook_id = session.get('etextbook_id')
    # Retrieve chapter data from form
    chapter_id = session.get('chapter_id')
    hide_section_id= "no"
    admin_id = session.get('user_id')
    chapter_list = fetch_chapters(etextbook_id, chapter_id)
    if chapter_list:
        status = add_section_to_db(section_id, chapter_id, etextbook_id, hide_section_id, admin_id, section_title)
        if status:
            session['section_id'] = section_id
            session['section_title'] = section_title
            # Flash message to confirm the chapter was saved
            flash("Chapter saved successfully!", "success")
            return redirect(url_for('admin.add_new_content_block'))  
        else:
            flash("Chapter was not saved!", "fail")
            return redirect(url_for('admin.admin_landing'))
    else:
        flash('Textbook with Id does not exist. Please enter a new one', 'error')

    flash("Section saved successfully!", "success")
    return redirect(url_for('admin.add_new_content_block'))

@admin_bp.route('/add_new_content_block')
def add_new_content_block():
    section_number = session.get('section_number')
    section_title = session.get('section_title')
    return render_template('add_new_content_block.html',section_number=section_number, section_title=section_title)

@admin_bp.route('/save_content_block', methods=['POST'])
def save_content_block():
    content_block_id = request.form.get('content_block_id')
    session['content_block_id'] = content_block_id  # Store content_block_id in session

    action = request.form.get('action')
    if action == 'add_text':
        return redirect(url_for('admin.add_text'))
    elif action == 'add_picture':
        return redirect(url_for('admin.add_picture'))
    elif action == 'add_activity':
        return redirect(url_for('admin.add_activity'))
    else:
        flash("Invalid action selected", "error")
        return redirect(url_for('admin.add_new_content_block'))

@admin_bp.route('/add_text')
def add_text():
    content_block_id = session.get('content_block_id')
    return render_template('add_text.html', content_block_id=content_block_id)

@admin_bp.route('/add_picture')
def add_picture():
    content_block_id = session.get('content_block_id')
    return render_template('add_picture.html', content_block_id=content_block_id)

@admin_bp.route('/add_activity')
def add_activity():
    content_block_id = session.get('content_block_id')
    return render_template('add_activity.html', content_block_id=content_block_id)

@admin_bp.route('/save_text', methods=['POST'])
def save_text():
    text = request.form.get('text')
    # Save the text content block (you would save it in the database)
    flash("Text added successfully!", "success")
    return redirect(url_for('admin.add_new_content_block'))

@admin_bp.route('/save_picture', methods=['POST'])
def save_picture():
    picture_url = request.form.get('picture')
    # Save the picture content block
    flash("Picture added successfully!", "success")
    return redirect(url_for('admin.add_new_content_block'))

@admin_bp.route('/save_activity', methods=['POST'])
def save_activity():
    activity_id = request.form.get('activity_id')
    session['activity_id'] = activity_id  # Store activity ID in session for adding questions
    return redirect(url_for('admin.add_question'))

@admin_bp.route('/add_question')
def add_question():
    activity_id = session.get('activity_id') 
    return render_template('add_question.html', activity_id=activity_id)

@admin_bp.route('/save_question', methods=['POST'])
def save_question():
    # Retrieve question and option details from the form
    question_id = request.form.get('question_id')
    question_text = request.form.get('question_text')
    
    # Option 1
    option1_text = request.form.get('option1_text')
    option1_explanation = request.form.get('option1_explanation')
    option1_label = request.form.get('option1_label')

    # Option 2
    option2_text = request.form.get('option2_text')
    option2_explanation = request.form.get('option2_explanation')
    option2_label = request.form.get('option2_label')

    # Option 3
    option3_text = request.form.get('option3_text')
    option3_explanation = request.form.get('option3_explanation')
    option3_label = request.form.get('option3_label')

    # Option 4
    option4_text = request.form.get('option4_text')
    option4_explanation = request.form.get('option4_explanation')
    option4_label = request.form.get('option4_label')

    # Here you would save the question and options to the database

    # Flash a success message and redirect to Add Activity page
    flash("Question added successfully!", "success")
    return redirect(url_for('admin.add_activity'))




@admin_bp.route('/modify_etextbook', methods=['GET', 'POST'])
def modify_etextbook():
    if request.method == 'POST':
        # Retrieve the E-textbook ID from the form
        etextbook_id = request.form.get('etextbook_id')
        
        # Store the E-textbook ID in the session
        session['etextbook_id'] = etextbook_id

        flash("E-textbook selected for modification.", "info")
        return redirect(url_for('admin.modify_etextbook'))

    return render_template('modify_etextbook.html')


@admin_bp.route('/add_new_chapter', methods=['GET', 'POST'])
def add_new_chapter():
    if request.method == 'POST':
        # Assuming we get a chapter name and other data from a form
        chapter_name = request.form.get('chapter_name')
        
        # Save the chapter details associated with the E-textbook ID
        etextbook_id = session.get('etextbook_id')
        # Logic to add the chapter to the specified E-textbook in the database

        flash(f"New chapter '{chapter_name}' added to E-textbook ID {etextbook_id}.", "success")
        return redirect(url_for('admin.modify_etextbook'))

    return render_template('new_chapter.html')

@admin_bp.route('/modify_chapter', methods=['GET', 'POST'])
def modify_chapter():
    if request.method == 'POST':
        # Assuming we get modified data from a form
        modified_data = request.form.get('modified_data')
        
        # Retrieve the E-textbook ID and update the relevant chapter
        etextbook_id = session.get('etextbook_id')
        # Logic to modify the chapter in the specified E-textbook in the database

        flash(f"Chapter modified for E-textbook ID {etextbook_id}.", "success")
        return redirect(url_for('admin.modify_etextbook'))

    return render_template('modify_chapter.html')

@admin_bp.route('/modify_section', methods=['GET', 'POST'])
def modify_section():
    if request.method == 'POST':
        section_number = request.form.get('section_number')
        session['section_number'] = section_number
        return redirect(url_for('admin.modify_content_block'))
    return render_template('modify_section.html')

@admin_bp.route('/modify_content_block', methods=['GET', 'POST'])
def modify_content_block():
    if request.method == 'POST':
        content_block_id = request.form.get('content_block_id')
        session['content_block_id'] = content_block_id
        flash(f"Content Block {content_block_id} modified.", "info")
        return redirect(url_for('admin.modify_section'))
    return render_template('modify_content_block.html')

@admin_bp.route('/create_active_course')
def create_active_course():
    return render_template('create_active_course.html')

@admin_bp.route('/save_active_course', methods=['POST'])
def save_active_course():
    # Retrieve form data
    course_id = request.form.get('course_id')
    course_name = request.form.get('course_name')
    etextbook_id = request.form.get('etextbook_id')
    faculty_id = request.form.get('faculty_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    token = request.form.get('token')
    capacity = request.form.get('capacity')

    # Save data logic here (e.g., save to the database)

    flash("Active course created successfully!", "success")
    return redirect(url_for('admin.admin_landing'))

@admin_bp.route('/create_evaluation_course')
def create_evaluation_course():
    return render_template('create_evaluation_course.html')

@admin_bp.route('/save_evaluation_course', methods=['POST'])
def save_evaluation_course():
    # Retrieve form data
    course_id = request.form.get('course_id')
    course_name = request.form.get('course_name')
    etextbook_id = request.form.get('etextbook_id')
    faculty_id = request.form.get('faculty_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Save data logic here (e.g., save to the database)

    flash("Evaluation course created successfully!", "success")
    return redirect(url_for('admin.admin_landing'))

  