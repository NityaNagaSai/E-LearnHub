from flask import render_template, redirect, url_for, request, flash, Blueprint, session, jsonify
from . import student_bp
from app.service import *
from app.blueprints.student.service import *
from collections import defaultdict
from datetime import datetime

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

# Student Landing Page
@student_bp.route('/landing_page', methods=['GET', 'POST'])
def landing():
    student_name = session.get('user_id', 'Student')
    choice = request.form.get("choice")
    if choice == "1":
        return redirect(url_for('student.display_sections'))
    elif choice == "2":
        return redirect(url_for('student.participation_points'))
    elif choice == "3":
        return redirect(url_for('main.index'))
    else:
        return render_template('student_landing.html', student_name = student_name)

# Student Sign-In Page
@student_bp.route('/student_signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        # Validating user (Student)
        status = validate_user(user_id, password, "Student")
        if status:
            session['user_id'] = user_id 
            return redirect(url_for('student.landing'))
        flash("Invalid login credentials!", "error")
    return render_template('/student_signin.html')

# Login Page
@student_bp.route('/student_login', methods=['GET', 'POST'])
def login():
    return render_template('/student_login.html')

# Display Sections
@student_bp.route('/content')
def display_sections():
    content_blocks = retrieve_blocks()
    # Dictionary structure to hold textbooks, chapters, sections, and content blocks
    content_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for content in content_blocks:
        textbook_id, textbook_title, chapter_id, chapter_title, section_id, section_title, content_block_id, content_type, content_text, is_activity = content
        content_dict[textbook_title][chapter_title][section_title].append({
            'textbook_id':textbook_id,
            'chapter_id':chapter_id,
            'section_id':section_id,
            'content_block_id': content_block_id,
            'content_type': content_type,
            'content_text': content_text
        })
    # Convert defaultdict back to a regular dict for easier template rendering
    content_dict = {k: dict(v) for k, v in content_dict.items()}
    return render_template('view_contents.html', content_dict=content_dict)

# Get Student Activity
@student_bp.route('/activity/<int:textbook_id>/<chapter_id>/<section_id>/<content_block_id>/<activity_id>')
def activity(textbook_id, chapter_id, section_id, content_block_id, activity_id):
    question_tuples = retrieve_questions(textbook_id, chapter_id, section_id, content_block_id, activity_id)
    # Convert tuples to dictionaries
    questions = [
        {
            "question_id": q[0],
            "question": q[1],
            "option1": q[2],
            "explanation_op1": q[3],
            "option2": q[4],
            "explanation_op2": q[5],
            "option3": q[6],
            "explanation_op3": q[7],
            "option4": q[8],
            "explanation_op4": q[9],
            "correct_answer": q[10]
        }
        for q in question_tuples
    ]
    return render_template(
        'student_activity.html', 
        questions=questions, 
        textbook_id=textbook_id, 
        chapter_id=chapter_id, 
        section_id=section_id, 
        content_block_id=content_block_id,
        activity_id=activity_id
    )

# Submit Sutdent Activity
def get_explanation(answer, explanation_op1, explanation_op2, explanation_op3, explanation_op4):
    if answer == '1':
        return explanation_op1
    elif answer == '2':
        return explanation_op2
    elif answer == '3':
        return explanation_op3
    elif answer == '4':
        return explanation_op4
    return ""

# Submit Answer
@student_bp.route('/submit_question/<int:textbook_id>/<chapter_id>/<section_id>/<content_block_id>/<activity_id>/<question_id>', methods=['POST'])
def submit_question(textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id):
    # Get the logged-in student ID from the session
    student_id = session.get('user_id')
    print(student_id)
    # Get the submitted answer
    submitted_answer = str(request.form.get('answer'))
    
    # Initialize variables for feedback
    explanation = ""
    points = 0

    # Retrieve course ID
    course_id = get_student_course_id(student_id)
    if not course_id:
        flash("You are not enrolled in any courses.", 'danger')
        return redirect(url_for('student.landing'))

    # Retrieve question details from the helper function
    question_data = get_question_details(textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id)
    if question_data:
        (question, explanation_op1,
             explanation_op2,explanation_op3, 
             explanation_op4, correct_answer) = question_data
        # Determine if the submitted answer is correct
        if submitted_answer.strip() == correct_answer.strip():
            flash("Correct! You've earned 3 points.", 'success')
            explanation = get_explanation(submitted_answer, explanation_op1, explanation_op2, explanation_op3, explanation_op4)
            points = 3
        else:
            flash("Incorrect. You've earned 1 point.", 'warning')
            explanation = f"The correct answer was '{correct_answer}': " + get_explanation(correct_answer, explanation_op1, explanation_op2, explanation_op3, explanation_op4)
            points = 1
    else:
        flash("Question not found.", 'danger')
    
    # Insert the result into StudentActivityPoint with a timestamp
    timestamp = datetime.now()
    save_student_activity_point(student_id, textbook_id, chapter_id, section_id, content_block_id, activity_id, question_id, points, timestamp)
    # Update the StudentParticipation table with new points and finished activities
    update_or_insert_student_participation(student_id,course_id)

    # Flash the explanation and score as additional messages
    flash(f"Explanation: {explanation}", 'info')
    flash(f"Points awarded: {points}", 'info')

    # Render the same page with flash messages displayed
    return redirect(url_for('student.activity', textbook_id=textbook_id, 
        chapter_id=chapter_id, 
        section_id=section_id, 
        content_block_id=content_block_id,
        activity_id=activity_id))

@student_bp.route('/participation_points')
def participation_points():
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('student.login'))
    student_id = session['user_id']
    print(student_id)
    # Get the student's enrolled course ID
    course_id = get_student_course_id(student_id)
    if not course_id:
        flash("You are not enrolled in any courses.", 'danger')
        return redirect(url_for('student.landing'))
    participation_data = get_student_participation_data(student_id, course_id)
    return render_template('student_participation.html',
                           student_points=participation_data['participation_points'],
                           finished_activities=participation_data['finished_activities'],
                           total_possible_points = participation_data['finished_activities']*3
                           )
