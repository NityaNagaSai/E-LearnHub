from flask import Blueprint

faculty_bp = Blueprint('faculty', __name__, template_folder='templates')

from app.blueprints.faculty import routes
