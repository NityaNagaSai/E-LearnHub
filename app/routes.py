from flask import render_template, redirect, url_for, request, flash, Blueprint, session

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/choose_role', methods=['POST'])
def choose_role():
    choice = request.form.get("choice")
    if choice == "1":
        return redirect(url_for('login.login', role="admin"))
    elif choice == "2":
        return redirect(url_for('login.login', role="faculty"))
    elif choice == "3":
        return redirect(url_for('login.login', role="ta"))
    elif choice == "4":
        return redirect(url_for('login.login', role="student"))
    elif choice == "5":
        shutdown_server()
    else:
        flash("Invalid choice. Please select a valid option.", "error")
        return redirect(url_for('index'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role') 
    
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        
        if role == 'admin':
            # add validation code
            return redirect(url_for(f'{role}.{role}_home'))
        elif role == 'faculty':
            # add validation code
            return redirect(url_for(f'{role}.{role}_home'))
        elif role == 'ta':
            # add validation code
            return redirect(url_for(f'{role}.{role}_home'))
        elif role == 'student':
            # add validation code
            return redirect(url_for(f'{role}.{role}_home'))

    return render_template('login.html', role=role)

def shutdown_server():
    pass