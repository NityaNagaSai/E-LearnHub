from flask import Blueprint, render_template, request, redirect, url_for, flash

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']  # Get the role from the form
        user_id = request.form['user_id']
        password = request.form['password']
        
        # Implement your authentication logic here
        # if authenticate(user_id, password, role):  # Replace with your authentication logic
        if role == 'admin':
            return redirect(url_for('admin.admin_landing'))  # Redirect to Admin landing page
        elif role == 'faculty':
            return redirect(url_for('faculty.faculty_landing'))  # Redirect to Faculty landing page
        elif role == 'ta':
            return redirect(url_for('ta.ta_landing'))  # Redirect to TA landing page
        elif role == 'student':
            return redirect(url_for('student.student_landing'))  # Redirect to Student landing page
        # else:
        #     flash('Login failed. Please check your credentials.')
    
    return render_template('login.html', role=request.args.get('role'))  # Pass role to the template
