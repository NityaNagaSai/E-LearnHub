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