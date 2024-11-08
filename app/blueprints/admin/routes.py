from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from . import admin_bp
import mysql.connector
from mysql.connector import errorcode
from app.blueprints.admin.service import *

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
        # action = request.form['action']
        
        status = create_new_faculty_account(first_name, last_name, email, password)
        if status:
            flash('New Faculty account created successfully!', 'success')
            return redirect(url_for('admin.admin_landing'))
        else:
            flash('An error occurred while creating the account. Please check your input and try again.', 'error')
            return render_template('create_faculty.html', first_name=first_name, last_name=last_name, email=email)


@admin_bp.route('/createetextbook')
def create_etextbook():
    return render_template('create_etextbook.html')

@admin_bp.route('/add_etextbook', methods=['POST'])
def add_etextbook():
    # Get form data
    title = request.form.get('title')
    etextbook_id = request.form.get('etextbook_id')
    
    # Check if eTextbook ID already exists
    etextbook_list = fetch_etextbooks(etextbook_id)
    print("Inside add_etextbook method:", etextbook_id)

    if etextbook_list:
        # Display an error message if eTextbook ID exists
        flash('A textbook with this ID already exists. Please enter a new one.', 'error')
        return redirect(url_for('admin.create_etextbook'))  # Redirect back to the form page for correction
    else:
        # Attempt to add eTextbook to the database
        status = add_etextbook_to_db(etextbook_id, title)
        if status:
            # Display a success message if eTextbook is added successfully
            flash('eTextbook added successfully!', 'success')

            # Store data in session and redirect to Add New Chapter page
            session['etextbook_title'] = title
            session['etextbook_id'] = etextbook_id
            return redirect(url_for('admin.new_chapter'))
        else:
            # Display a general error message if there was an issue adding the eTextbook
            flash('There was an error adding the eTextbook. Please try again.', 'error')
            return redirect(url_for('admin.create_etextbook'))

    # Redirect back to the form if there’s any other issue
    return redirect(url_for('admin.create_etextbook'))


@admin_bp.route('/createetextbook/newchapter')
def new_chapter():
    etextbook_title = session.get('etextbook_title')
    etextbook_id = session.get('etextbook_id')
    return render_template('new_chapter.html', etextbook_title=etextbook_title, etextbook_id=etextbook_id, call_type="new")


@admin_bp.route('/save_chapter', methods=['POST'])
def save_chapter():
    etextbook_id = session.get('etextbook_id')
    chapter_id = request.form.get('chapter_id')
    chapter_title = request.form.get('chapter_title')
    hide_chap_id = "no"
    admin_id = session.get('user_id')
    
    # Check if the eTextbook ID exists
    etextbook_list = fetch_etextbooks(etextbook_id)
    if etextbook_list:
        # Attempt to save the chapter to the database
        status = add_chapter_to_db(chapter_id, etextbook_id, hide_chap_id, admin_id, chapter_title)
        if status:
            # Save chapter details to session and display success message
            session['chap_id'] = chapter_id
            session['chap_title'] = chapter_title
            flash("Chapter saved successfully!", "success")
            return redirect(url_for('admin.add_new_section'))  # Redirect to Add New Section page
        else:
            # Display error if chapter could not be saved
            flash("There was an error saving the chapter. Please try again.", "error")
            return redirect(url_for('admin.new_chapter'))  # Redirect back to chapter creation form
    else:
        # Display error if eTextbook ID does not exist
        flash("The specified eTextbook ID does not exist. Please verify and try again.", "error")
        return redirect(url_for('admin.new_chapter'))  # Redirect back to chapter creation form

    # Redirect to admin landing if none of the conditions are met
    return redirect(url_for('admin.admin_landing'))



@admin_bp.route('/add_new_section')
def add_new_section():
    chapter_id = session.get('chap_id')
    chapter_title = session.get('chap_title')
    return render_template('add_new_section.html', chapter_id=chapter_id, chapter_title=chapter_title, call_type="new")

@admin_bp.route('/save_section', methods=['POST'])
def save_section():
    section_id = request.form.get('section_number')
    section_title = request.form.get('section_title')
    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    admin_id = session.get('user_id')
    hide_section_id = "no"
    chapter_list = fetch_chapters(etextbook_id, chapter_id)
    if chapter_list:
        status = add_section_to_db(section_id, chapter_id, etextbook_id, hide_section_id, admin_id, section_title)
        if status:
            session['section_id'] = section_id
            session['section_title'] = section_title
            flash("Section saved successfully!", "success")
            return redirect(url_for('admin.add_new_content_block', section_number=section_id))
        else:
            flash("Failed to save the section. Please try again.", "error")
            return redirect(url_for('admin.add_new_section'))
    else:
        flash("Chapter does not exist. Please check the chapter ID and try again.", "error")
    return redirect(url_for('admin.admin_landing'))


@admin_bp.route('/add_new_content_block')
def add_new_content_block():
    section_number = session.get('section_id')
    section_title = session.get('section_title')
    return render_template('add_new_content_block.html',section_number=section_number, section_title=section_title, call_type="new")

@admin_bp.route('/save_content_block', methods=['POST'])
def save_content_block():
    content_block_id = request.form.get('content_block_id')
    session['content_block_id'] = content_block_id
    action = request.form.get('action')
    if action == 'add_text':
        return redirect(url_for('admin.add_text', call_type="new"))
    elif action == 'add_picture':
        return redirect(url_for('admin.add_picture', call_type="new"))
    elif action == 'add_activity':
        return redirect(url_for('admin.add_activity', call_type="new"))
    else:
        flash("Invalid action selected", "error")
        return redirect(url_for('admin.add_new_content_block'))

@admin_bp.route('/add_text')
def add_text():
    call_type = request.args.get('call_type')
    print("inside add_text method")
    print(call_type)
    content_block_id = session.get('content_block_id')
    return render_template('add_text.html', content_block_id=content_block_id, call_type = call_type)

@admin_bp.route('/add_picture')
def add_picture():
    call_type = request.args.get('call_type')
    content_block_id = session.get('content_block_id')
    return render_template('add_picture.html', content_block_id=content_block_id, call_type = call_type)

@admin_bp.route('/add_activity')
def add_activity():
    call_type = request.args.get('call_type')
    print(call_type)
    content_block_id = session.get('content_block_id')
    return render_template('add_activity.html', content_block_id=content_block_id, call_type=call_type)

@admin_bp.route('/save_text', methods=['POST'])
def save_text():
    text = request.form.get('text')
    print("Inside save_text method")
    section_id = session.get('section_id')
    content_block_id = session.get('content_block_id')
    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    admin_id = session.get('user_id')
    is_hidden= "no"
    call_type = request.form.get('call_type')
    print("Inside save_text:", call_type)
    # print(section_id)
    # print(content_block_id)
    # print(etextbook_id)
    # print(chapter_id)
    # print(admin_id)
    content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
    print("After fetch_content_blocks")
    if content_block_list:
        delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
        print("After delete_status")

        if delete_status:
            status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'text', text)
            print("After add_content_to_db")

            if status:
                flash("Text saved successfully!", "success")
                if call_type == "modify":
                    return redirect(url_for('admin.modify_content_block')) 
                return redirect(url_for('admin.add_new_content_block'))  
            else:
                flash("Text was not saved!", "fail")
                if call_type == "modify":
                    return redirect(url_for('admin.modify_content_block')) 
                return redirect(url_for('admin.add_new_content_block'))
        else:
            flash("Text was not saved!", "fail")
            if call_type == "modify":
                    return redirect(url_for('admin.modify_content_block')) 
            return redirect(url_for('admin.add_new_content_block'))
    else:
        status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'text', text)
        print(section_id)
        print("Inside content_block_list else block")
        if status:
            flash("Text saved successfully!", "success")
            if call_type == "modify":
                return redirect(url_for('admin.modify_content_block')) 
            return redirect(url_for('admin.add_new_content_block'))  
        else:
            flash("Text was not saved!", "fail")
            if call_type == "modify":
                    return redirect(url_for('admin.modify_content_block')) 
            return redirect(url_for('admin.add_new_content_block'))

@admin_bp.route('/save_modified_text', methods=['POST'])
def save_modified_text():
    modified_text = request.form.get('text')
    content_block_id = session.get('content_block_id')
    section_id = session.get('section_id')
    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    admin_id = session.get('user_id')
    is_hidden = "no"
    section_list = fetch_sections(etextbook_id, chapter_id, section_id)
    if section_list:
        status = update_content_in_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'text', modified_text)
        
        if status:
            flash("Content block modified successfully!", "success")
            return redirect(url_for('admin.modify_content_block'))
        else:
            flash("Failed to modify content block!", "error")
            return redirect(url_for('admin.modify_content_block'))
    else:
        flash("Textbook with the given ID does not exist. Please enter a valid one.", "error")
    
    return redirect(url_for('admin.admin_landing'))


@admin_bp.route('/save_picture', methods=['POST'])
def save_picture():
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

    call_type = request.form.get('call_type')

    content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
    print("Inside save_picture method:", content_block_list)
    if content_block_list:
        delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
        print(delete_status)
        if delete_status:
            status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'image', picture_url)
            if status:
                flash("Picture saved successfully!", "success")
                if call_type == "modify":
                    return redirect(url_for('admin.modify_content_block')) 

                return redirect(url_for('admin.add_new_content_block'))  
            else:
                flash("Picture was not saved!", "fail")
                return redirect(url_for('admin.add_new_content_block'))
        else:
            flash("Picture was not saved!", "fail")
            return redirect(url_for('admin.add_new_content_block'))
    else:
        status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'image', picture_url)
        if status:
            flash("Picture saved successfully!", "success")
            return redirect(url_for('admin.add_new_content_block'))  
        else:
            flash("Picture was not saved!", "fail")
            return redirect(url_for('admin.add_new_content_block'))


@admin_bp.route('/save_modified_picture', methods=['POST'])
def save_modified_picture():
    # Assuming the new picture will be saved as "sample2.png"
    picture_url = "sample2.png"
    
    # Set up session and other necessary variables
    section_id = session.get('section_id')
    content_block_id = session.get('content_block_id')
    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    admin_id = session.get('user_id')
    is_hidden = "no"
    
    # Check if the section exists in the database
    section_list = fetch_sections(etextbook_id, chapter_id, section_id)
    if section_list:
        # Update the picture URL in the existing content block
        status = update_content_in_db(content_block_id, section_id, chapter_id, etextbook_id, is_hidden, admin_id, 'image', picture_url)
        
        if status:
            flash("Picture modified successfully!", "success")
            return redirect(url_for('admin.modify_content_block'))
        else:
            flash("Failed to modify picture.", "error")
            return redirect(url_for('admin.modify_content_block'))
    else:
        flash('Textbook with the given ID does not exist. Please enter a new one.', 'error')
    
    return redirect(url_for('admin.admin_landing'))


@admin_bp.route('/save_activity', methods=['POST'])
def save_activity():
    activity_id = request.form.get('activity_id')
    session['activity_id'] = activity_id
    section_id = session.get('section_id')
    content_block_id = session.get('content_block_id')
    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    admin_id = session.get('user_id')

    call_type = request.form.get('call_type')


    print("inside save_activity method:",etextbook_id)
    content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
    if content_block_list:
        content_type = content_block_list[0][4]
        if content_type == 'activity':
            activity_data = fetch_activity(etextbook_id, chapter_id, section_id, content_block_id, activity_id)
            if activity_data:
                return redirect(url_for('admin.add_question', call_type=call_type))
            else:
                status = add_activity_to_db(etextbook_id, chapter_id, section_id, content_block_id, 
                                            activity_id, "no", admin_id)
                if status:
                    return redirect(url_for('admin.add_question', call_type=call_type))
                else:
                    flash("Error in saving the activity. Please try again.", "error")
                    return redirect(url_for('admin.add_activity', call_type=call_type))   
        else:
            delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
            if delete_status:
                status = add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, 'no', admin_id, 'activity', activity_id)
                if status:
                    flash("Activity saved successfully!", "success")
                    return redirect(url_for('admin.add_question', call_type=call_type))
                else:
                    flash("Error in saving the activity. Please try again.", "error")
                    return redirect(url_for('admin.add_activity', call_type=call_type))   
            else:
                flash("Error in saving the activity. Please try again.", "error")
                return redirect(url_for('admin.add_question', call_type=call_type))         
    else:
        if add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, 'no', admin_id, 'activity', activity_id):
            status = add_activity_to_db(etextbook_id, chapter_id, section_id, content_block_id, 
                                            activity_id, "no", admin_id)
            if status:
                flash("Activity saved successfully!", "success")
                return redirect(url_for('admin.add_question', call_type=call_type))
            else:
                flash("Error in saving the activity. Please try again.", "error")
                return redirect(url_for('admin.add_activity', call_type=call_type))
        else:
            flash("Error in saving the Block. Please try again.", "error")
            return redirect(url_for('admin.add_activity', call_type=call_type))


@admin_bp.route('/save_modified_activity', methods=['POST'])
def save_modified_activity():
    activity_id = request.form.get('activity_id')
    session['activity_id'] = activity_id  # Store activity ID in session for adding questions
    section_id = session.get('section_id')
    content_block_id = session.get('content_block_id')
    etextbook_id = session.get('etextbook_id')
    chapter_id = session.get('chap_id')
    admin_id = session.get('user_id')

    content_block_list = fetch_content_blocks(etextbook_id, chapter_id, section_id, content_block_id)
    if content_block_list:
        delete_status = delete_content(etextbook_id, chapter_id, section_id, content_block_id)
        if delete_status:
            activity_data = fetch_activity(etextbook_id, chapter_id, section_id, content_block_id, activity_id)
            if activity_data:
                flash("Activity with this ID already exists. Please enter a unique ID.", "error")
                return redirect(url_for('admin.add_question'))
            else:
                if add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, 'no', admin_id, 'activity', activity_id):
                    status = add_activity_to_db(etextbook_id, chapter_id, section_id, content_block_id, 
                                                activity_id, "no", admin_id)
                    if status:
                        flash("Activity modified and saved successfully!", "success")
                        return redirect(url_for('admin.add_question'))
                    else:
                        flash("Error in saving the activity. Please try again.", "error")
                        return redirect(url_for('admin.add_activity'))
                else:
                    flash("Error in saving the Block. Please try again.", "error")
                    return redirect(url_for('admin.add_activity'))
        # flash("Activity with the entered ID already exists. Please enter a unique ID", "error")
        # return redirect(url_for('admin.add_activity'))
    else:
        if add_content_to_db(content_block_id, section_id, chapter_id, etextbook_id, 'no', admin_id, 'activity', activity_id):
            status = add_activity_to_db(etextbook_id, chapter_id, section_id, content_block_id, 
                                            activity_id, "no", admin_id)
            if status:
                flash("New activity saved successfully!", "success")
                return redirect(url_for('admin.add_question'))
            else:
                flash("Error in saving the activity. Please try again.", "error")
                return redirect(url_for('admin.add_activity'))
        else:
            flash("Error in saving the Block. Please try again.", "error")
            return redirect(url_for('admin.add_activity'))
        
    # activity_id = request.form.get('activity_id')
    # session['activity_id'] = activity_id  # Store activity ID in session for adding questions
    # return redirect(url_for('admin.modify_question'))


@admin_bp.route('/add_question')
def add_question():
    activity_id = session.get('activity_id') 
    call_type = request.args.get('call_type')
    print(call_type)
    return render_template('add_question.html', activity_id=activity_id, call_type=call_type)

@admin_bp.route('/save_question', methods=['POST'])
def save_question():

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

    call_type = request.form.get('call_type')
    print("inside save_question:",call_type)
    
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
        return redirect(url_for('admin.add_question', call_type=call_type))
    else:
        status = add_activity_question(question_id, activity_id, content_block_id, etextbook_id, section_id, chapter_id,
                                       question_text, correct_answer, option1_text, option2_text, option3_text, option4_text,
                                       option1_explanation, option2_explanation, option3_explanation, option4_explanation)
        if status:
            flash("Question added successfully!", "success")
            return redirect(url_for('admin.add_activity', call_type=call_type))
        else:
            flash("Error in adding the question", "error")
            return redirect(url_for('admin.add_question', call_type=call_type))


@admin_bp.route('/modify_question')
def modify_question():
    activity_id = session.get('activity_id')
    question_id = session.get('question_id')
    return render_template(
        'modify_question.html')

@admin_bp.route('/save_modified_question', methods=['POST'])
def save_modified_question():
    flash("Question modified successfully!", "success")
    return redirect(url_for('admin.modify_activity'))


@admin_bp.route('/modify_etextbook', methods=['GET', 'POST'])
def modify_etextbook():
    if request.method == 'POST':
        # Retrieve the E-textbook ID from the form
        etextbook_id = request.form.get('etextbook_id')
        # Store the E-textbook ID in the session
        session['etextbook_id'] = etextbook_id
        print("Inside modify_textbook method:", etextbook_id)

        etextbook_list = fetch_etextbooks(etextbook_id)
        if etextbook_list:
            title = etextbook_list[0][1]
            action = request.form.get('action')
            if action == "add_chapter":
                flash("E-textbook found. Ready to add a new chapter.", "info")
                return render_template('new_chapter.html', etextbook_title=title, etextbook_id=etextbook_id, call_type='modify')
            elif action == "modify_chapter":
                flash("E-textbook found. Ready to modify chapters.", "info")
                return redirect(url_for('admin.modify_chapter'))
        else:
            flash('Textbook with Id does not exists. Please enter a new one', 'error')
            return redirect(url_for('admin.modify_etextbook'))

    return render_template('modify_etextbook.html')


# @admin_bp.route('/add_new_chapter', methods=['GET', 'POST'])
# def add_new_chapter():
#     if request.method == 'POST':
#         # Assuming we get a chapter name and other data from a form
#         chapter_name = request.form.get('chapter_name')
        
#         # Save the chapter details associated with the E-textbook ID
#         etextbook_id = session.get('etextbook_id')
#         # Logic to add the chapter to the specified E-textbook in the database

#         flash(f"New chapter '{chapter_name}' added to E-textbook ID {etextbook_id}.", "success")
#         return redirect(url_for('admin.modify_etextbook'))

#     return render_template('new_chapter.html')

@admin_bp.route('/modify_chapter', methods=['GET', 'POST'])
def modify_chapter():
    if request.method == 'POST':
        # Assuming we get modified data from a form
        # modified_data = request.form.get('modified_data')
        # Retrieve the E-textbook ID and update the relevant chapter
        etextbook_id = session.get('etextbook_id')
        chapter_id = request.form.get('chapter_id')
        session['chap_id'] = chapter_id
        action = request.form.get('action')
        print(etextbook_id, chapter_id)
        # Logic to modify the chapter in the specified E-textbook in the database
        chapter_list = fetch_chapters(etextbook_id, chapter_id)
        if chapter_list:
            if action == "add_new_section":
                flash("Chapter found. Ready to add a new section.", "info")
                return redirect(url_for('admin.add_new_section'))
            elif action == "modify_section":
                flash("Chapter found. Ready to modify existing sections.", "info")
                return redirect(url_for('admin.modify_section'))
        else:
            flash("No chapter exists with the current chapter id. Please try again.", "error")
            return redirect(url_for('admin.modify_chapter'))

    return render_template('modify_chapter.html')

@admin_bp.route('/modify_section', methods=['GET', 'POST'])
def modify_section():
    # if request.method == "GET":
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
                flash("Section found. Ready to add a new content block.", "info")
                return redirect(url_for("admin.add_new_content_block"))
            elif action == "modify_content_block":
                flash("Section found. Ready to modify content blocks.", "info")
                return redirect(url_for("admin.modify_content_block"))
        else:
            flash(f"Section number {section_number} does not exist. Please try again", "error")
            return redirect(url_for('admin.modify_section'))
    return render_template('modify_section.html', etextbook_id = etextbook_id, chapter_id=chapter_id)

@admin_bp.route('/modify_content_block', methods=['GET', 'POST'])
def modify_content_block():
    if request.method == 'POST':
        content_block_id = request.form.get('content_block_id')
        session['content_block_id'] = content_block_id  # Store content_block_id in session

        action = request.form.get('action')
        if action == 'modify_text':
            return redirect(url_for('admin.add_text', call_type="modify"))
        elif action == 'modify_picture':
            return redirect(url_for('admin.add_picture', call_type="modify"))
        elif action == 'modify_activity':
            return redirect(url_for('admin.add_activity', call_type="modify"))
        else:
            flash("Invalid action selected", "error")
            return redirect(url_for('admin.modify_content_block'))
        # content_block_id = request.form.get('content_block_id')
        # session['content_block_id'] = content_block_id
        # flash(f"Content Block {content_block_id} modified.", "info")
        # return redirect(url_for('admin.modify_section'))
    return render_template('modify_content_block.html')

@admin_bp.route('/modify_text', methods=['GET', 'POST'])
def modify_text():
    content_block_id = session.get('content_block_id')    
    if request.method == 'POST':
        modified_text = request.form.get('text')
        status = update_content_in_db(content_block_id, modified_text)   
        if status:
            flash("Content modified successfully!", "success")
            return redirect(url_for('admin.modify_content_block'))
        else:
            flash("Failed to modify content.", "error")
    
    return render_template('modify_text.html',content_block_id=content_block_id)



@admin_bp.route('/modify_picture', methods=['GET', 'POST'])
def modify_picture():
    content_block_id = session.get('content_block_id')
    if request.method == 'POST':
        modified_picture_url = request.form.get('picture_url')
    return render_template('modify_picture.html')

@admin_bp.route('/modify_activity', methods=['GET', 'POST'])
def modify_activity():
    content_block_id = session.get('content_block_id')
    if request.method == 'POST':
        modified_activity = request.form.get('activity')
    return render_template('modify_activity.html')



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
    status = add_new_course(course_id, course_name, 'Active', etextbook_id, faculty_id, start_date, end_date, token, capacity)
    
    if status:
        flash("Active course created successfully!", "success")
        return redirect(url_for('admin.admin_landing'))
    else:
        flash("There was an error in creating the course. Please try again", "error")
        return redirect(url_for('admin.create_active_course'))


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
    status = add_new_course(course_id, course_name, 'Evaluation', etextbook_id, faculty_id, start_date, end_date, None, None)
    if status:
        flash("Evaluation course created successfully!", "success")
        return redirect(url_for('admin.admin_landing'))
    else:
        flash("There was an error in creating the course. Please try again", "error")
        return redirect(url_for('admin.create_evaluation_course'))

@admin_bp.route('/logout')
def logout():
    print("Inside logout method")
    session.clear()
    return redirect(url_for('main.index'))


  