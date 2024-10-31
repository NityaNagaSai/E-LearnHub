from flask import render_template, redirect, url_for, request, flash, Blueprint, session
from . import student_bp
import os
import json

# Mock data structures
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
STUDENTS_FILE = os.path.join(BASE_DIR, 'students.json')
ENROLLMENTS_FILE = os.path.join(BASE_DIR, 'enrollments.json')

def load_data(file_path):
    """Load data from the specified JSON file."""
    if not os.path.exists(file_path):
        return []  # Return an empty list if the file doesn't exist

    with open(file_path, 'r') as f:
        return json.load(f)  # Load data from the file

def save_data(file_path, data):
    """Save data back to the specified JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)  # Write data back to the file

# Load the initial data
students = load_data(STUDENTS_FILE)
enrollments = load_data(ENROLLMENTS_FILE)

@student_bp.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        course_token = request.form['course_token']
        full_name = f"{first_name} {last_name}"

        # Check if the student exists by email
        student_found = False
        student_id = None
        for student in students:
            if student["email"] == email:
                student_id = student["student_id"]
                student_found = True
                break
        if not student_found:
            flash("Student does not exist! Please check the name or email!")
            return render_template('student_enrollment.html')  # Return to the form
        # Check if the student is already enrolled in the course
        already_enrolled = False
        for enrollment in enrollments:
            if enrollment["course_token"] == course_token and enrollment["student_id"] == student_id:
                already_enrolled = True
                if enrollment["status"] == "Enrolled":
                    flash("You are already enrolled in this course.")
                else:
                    flash("Your enrollment request is already pending.")
                break
        if not already_enrolled:
            new_enrollment = {
                "course_token": course_token,
                "student_id": student_id,
                "status": "Pending"
            }
            enrollments.append(new_enrollment)  # Append the new enrollment
            flash("Enrollment request submitted. You are on the waiting list.")
    
    save_data(STUDENTS_FILE,students)
    save_data(ENROLLMENTS_FILE, enrollments)
    print(enrollments)
    print(students)
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

@student_bp.route('/student_signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        for s in students:
            if s["student_id"] == user_id and s["password"] == password:
                session["student_name"] = s["full_name"]
                return redirect(url_for('student.landing'))
        flash("Invalid login credentials!")
    return render_template('/student_signin.html')

@student_bp.route('/student_login', methods=['GET', 'POST'])
def login():
    return render_template('/student_login.html')

@student_bp.route('/choose_option', methods=['POST'])
def choose_option():
    choice = request.form.get("choice")
    if choice == "1":
        return redirect(url_for('student.enroll'))
    elif choice == "2":
        return redirect(url_for('student.signin'))
    elif choice == "3":
        # End the program
        return redirect(url_for('main.index'))
    else:
        flash("Invalid choice. Please select a valid option.", "error")
        return redirect(url_for('student.login'))

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
