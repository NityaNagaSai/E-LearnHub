from flask import render_template, redirect, url_for, request, flash, Blueprint, session
from app.service import *

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def index():
    session.clear()  
    return render_template('index.html')

@main_bp.route('/choose_role', methods=['GET'])
def choose_role():
    choice = request.args.get("choice")
    if choice == "1":
        return redirect(url_for('main.login', role="admin"))
    elif choice == "2":
        return redirect(url_for('main.login', role="faculty"))
    elif choice == "3":
        return redirect(url_for('main.login', role="ta"))
    elif choice == "4":
        return redirect(url_for('student.login'))
    elif choice == "5":
        # Handle exit or end the session as needed
        flash("Exiting the platform.", "info")
        return redirect(url_for('index'))  # Redirect to home or exit page
    else:
        flash("Invalid choice. Please select a valid option.", "error")
        return redirect(url_for('main.index'))
    
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        role = request.args.get('role') 
    
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        role = request.form.get('role') 

        if role == 'admin':
            status = validate_user(user_id, password, role)
            session['user_id'] = user_id
            if status:
                return redirect(url_for(f'{role}.{role}_landing'))
        elif role == 'faculty':
            status = validate_user(user_id, password, role)
            session['user_id'] = user_id
            if status:
                return redirect(url_for(f'{role}.{role}_home'))
        elif role == 'ta':
            # add validation code
            status = validate_user(user_id, password, role)
            session['user_id'] = user_id
            if status:
                return redirect(url_for(f'{role}.{role}_landing'))
        elif role == 'student':
            # add validation code - added in the actual student login
            return redirect(url_for(f'{role}.{role}_landing'))
        flash("Login Incorrect. Please try again.")
    return render_template('login.html', role=role)


@main_bp.route('/retrieval_queries', methods=['GET', 'POST'])
def retrieval_queries():
    if request.method == 'GET':
        return render_template('retrieval_queries.html')
    if request.method == 'POST':
        option = request.form.get('option')
        if option == 1:
            pass
        if option == 2:
            data = retrieval_sql_query2()

        if option == 3:
            pass
        if option == 4:
            pass
        if option == 5:
            pass
        if option == 6:
            pass
        if option == 7:
            pass

