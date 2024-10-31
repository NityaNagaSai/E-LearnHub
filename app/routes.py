from flask import render_template, redirect, url_for, request, flash, Blueprint

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
        return redirect(url_for('student.login', role="student"))
    elif choice == "5":
        # End the program
        return
    else:
        flash("Invalid choice. Please select a valid option.", "error")
        return redirect(url_for('index'))
