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
        option = int(request.form.get('option'))
        
        if option == 1:
            section_count = retrieval_sql_query1(101)[0][0]
            return render_template('query1_result.html', section_count=section_count, textbook_id=101)
        
        elif option == 2:
            data = retrieval_sql_query2()
            return render_template('query2_result.html', data=data)
        
        elif option == 3:
            data = retrieval_sql_query3()
            return render_template('query3_result.html', data=data)
        
        elif option == 4:
            data = retrieval_sql_query4()
            return render_template('query4_result.html', data=data)
        
        elif option == 5:
            data = retrieval_sql_query5()
            return render_template('query5_result.html', data=data)
        
        elif option == 6:
            data, op = retrieval_sql_query6()
            return render_template('query6_result.html', options=data, correct_answer= int(op))
        
        elif option == 7:
            data = retrieval_sql_query7()
            return render_template('query7_result.html', data=data)
        
        else:
            flash("Invalid option selected.", "error")
            return redirect(url_for('main.retrieval_queries'))

