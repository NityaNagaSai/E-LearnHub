from flask import Flask
from app.routes import main_bp
from app.blueprints.ta import ta_bp
from app.blueprints.faculty import faculty_bp
from app.blueprints.admin import admin_bp
from app.blueprints.student import student_bp
from app.db.crud import db_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = "dbmsproject"
    app.register_blueprint(main_bp)
    app.register_blueprint(ta_bp, url_prefix="/ta")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(db_bp, url_prefix="/db")

    return app

