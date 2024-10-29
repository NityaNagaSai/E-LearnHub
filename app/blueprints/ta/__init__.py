from flask import Blueprint

ta_bp = Blueprint('ta', __name__, template_folder='templates')

from app.blueprints.ta import routes
