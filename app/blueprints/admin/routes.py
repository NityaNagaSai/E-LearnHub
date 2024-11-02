from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify,session

from . import admin_bp
import mysql.connector
from mysql.connector import errorcode

@admin_bp.route('/home')
def admin_landing():
    return render_template('admin_landing.html')

@admin_bp.route('/createfaculty')
def create_faculty():
    return render_template('create_faculty.html')

@admin_bp.route('/createetextbook')
def create_etextbook():
    return render_template('create_etextbook.html')

@admin_bp.route('/createetextbook/newchapter')
def new_chapter():
    etextbook_title = session.get('etextbook_title')
    etextbook_id = session.get('etextbook_id')

    # Render the Add New Chapter page with the e-textbook data
    return render_template('new_chapter.html', etextbook_title=etextbook_title, etextbook_id=etextbook_id)

@admin_bp.route('/add_etextbook', methods=['POST'])
def add_etextbook():
    # Get form data
    title = request.form.get('title')
    etextbook_id = request.form.get('etextbook_id')

    # Store data in the session (or save to database as needed)
    session['etextbook_title'] = title
    session['etextbook_id'] = etextbook_id

    # Redirect to the Add New Chapter page
    return redirect(url_for('admin.new_chapter'))

@admin_bp.route('/save_chapter', methods=['POST'])
def save_chapter():
    # Retrieve previous e-textbook data from session
    etextbook_title = session.get('etextbook_title')
    etextbook_id = session.get('etextbook_id')

    # Retrieve chapter data from form
    chapter_id = request.form.get('chapter_id')
    chapter_title = request.form.get('chapter_title')

    # Save the chapter data (you can implement database saving here)
    # For example:
    # db.save_chapter(etextbook_id, chapter_id, chapter_title)

    # Flash message to confirm the chapter was saved
    flash("Chapter saved successfully!", "success")

    # Redirect to the Add New Section page
    return redirect(url_for('admin.add_new_section'))

@admin_bp.route('/add_new_section')
def add_new_section():
    # This route should render the page for adding a new section.
    # Add any data retrieval needed for the Add New Section page.
    return render_template('add_new_section.html')


@admin_bp.route('/save_section', methods=['POST'])
def save_section():
    # Retrieve section data from form
    section_number = request.form.get('section_number')
    section_title = request.form.get('section_title')

    # Retrieve the current chapter ID from the session
    chapter_id = session.get('chapter_id')

    # Save the section data here (e.g., to a database)
    # db.save_section(chapter_id, section_number, section_title)

    flash("Section saved successfully!", "success")

    # Redirect to the Add New Content Block page
    return redirect(url_for('admin.add_new_content_block'))

@admin_bp.route('/add_new_content_block')
def add_new_content_block():
    # Render the page for adding a new content block
    return render_template('add_new_content_block.html')

@admin_bp.route('/save_content_block', methods=['POST'])
def save_content_block():
    content_block_id = request.form.get('content_block_id')
    action = request.form.get('action')

    # Save content block data (implement database saving if needed)

    # Redirect based on the selected action
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
    return render_template('add_text.html')

@admin_bp.route('/add_picture')
def add_picture():
    return render_template('add_picture.html')

@admin_bp.route('/add_activity')
def add_activity():
    return render_template('add_activity.html')


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
    return render_template('add_question.html')

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