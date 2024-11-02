from flask import render_template, redirect, url_for, request, flash, Blueprint, session
from . import student_bp
from app.service import validate_user, enroll_student
import os
import json

# Student Enrollment
@student_bp.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        course_token = request.form['course_token']
        status = enroll_student(first_name, last_name, email, password, course_token)
        if status == "Created":
            flash("Enrollment request submitted. You are on the waiting list.", "success")
        elif status == "Pending":
            flash("Your enrollment request is already pending.", "error")
        else:
            flash("You are already enrolled in this course.", "error")
    return render_template('student_enrollment.html')

@student_bp.route('/landing_page', methods=['GET', 'POST'])
def landing():
    student_name = session.get('student_name', 'Student')
    choice = request.form.get("choice")
    if choice == "1":
        return redirect(url_for('student.view_section'))
    elif choice == "2":
        return redirect(url_for('student.view_participation'))
    elif choice == "3":
        return redirect(url_for('main.index'))
    else:
        return render_template('student_landing.html', student_name = student_name)

# Student Sign In Page
@student_bp.route('/student_signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        # Validating user (Student)
        status = validate_user(user_id, password, "Student")
        if status:
            return redirect(url_for('student.landing'))
        flash("Invalid login credentials!", "error")
    return render_template('/student_signin.html')

# Login Page
@student_bp.route('/student_login', methods=['GET', 'POST'])
def login():
    return render_template('/student_login.html')

@student_bp.route('/sections')
def view_section():
    textbooks = [
        {
            "id": 1, "title": "Textbook 1",
            "chapters": [
                {
                    "id": 1, "title": "Introduction to Programming",
                    "sections": [
                        {"id": 1, "title": "Getting Started", "blocks": [{"id": 1, "title": "Introduction"}]},
                        {"id": 2, "title": "Basic Syntax", "blocks": [{"id": 2, "title": "Variables"}, {"id": 3, "title": "Data Types"}]}
                    ]
                },
                {
                    "id": 2, "title": "Advanced Topics",
                    "sections": [
                        {"id": 3, "title": "OOP Basics", "blocks": [{"id": 4, "title": "Classes and Objects"}]}
                    ]
                }
            ]
        }
    ]
    return render_template('view_contents.html', textbooks=textbooks)
