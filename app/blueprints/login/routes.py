from flask import render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template


from app.blueprints.login import login_bp


admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/admin_landing')
def admin_landing():
    return render_template('admin_landing.html')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role', 'student')  # default role is 'student'
    
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        
        # Validate user based on role
        # Example: using mock user data for demonstration
        mock_users = {
            "admin": {"password": "adminpass", "role": "admin"},
            "faculty": {"password": "facultypass", "role": "faculty"},
            "ta": {"password": "tapass", "role": "ta"},
            "student": {"password": "studentpass", "role": "student"}
        }
        
        if user_id in mock_users and mock_users[user_id]["password"] == password and mock_users[user_id]["role"] == role:
            session['user_role'] = role
            return redirect(url_for(f'{role}.{role}_home'))
        else:
            flash("Login Incorrect", "error")
            return redirect(url_for('login.login', role=role))

    return render_template('login.html', role=role)
