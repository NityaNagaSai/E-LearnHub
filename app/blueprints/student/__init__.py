from flask import Blueprint

student_bp = Blueprint('student', __name__, template_folder='templates')

from app.blueprints.student import routes
