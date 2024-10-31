from flask import Flask
from app.routes import main_bp
from app.blueprints.ta import ta_bp
from app.blueprints.login import login_bp
from app.blueprints.faculty import faculty_bp
from app.blueprints.admin import admin_bp
from app.db.create_tables import create_tables

# from app.blueprints.login import login_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp, url_prefix="/login")
    app.register_blueprint(ta_bp, url_prefix="/ta")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    # app.register_blueprint(db_bp, url_prefix="/db")

    with app.app_context():
        create_tables()

    return app