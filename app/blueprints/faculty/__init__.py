from flask import Blueprint

faculty_bp = Blueprint('faculty', __name__, template_folder='templates', url_prefix='/faculty')

from app.blueprints.faculty import routes


