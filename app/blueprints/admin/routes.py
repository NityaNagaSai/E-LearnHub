from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import admin_bp
import mysql.connector
from mysql.connector import errorcode
from app.blueprints.admin.service import create_new_faculty_account


@admin_bp.route('/home')
def admin_landing():
    return render_template('admin_landing.html')

@admin_bp.route('/create_faculty_account', methods=["GET", "POST"])
def create_faculty_account():
    if request.method == "GET":
        return render_template('create_faculty.html')
    elif request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        action = request.form['action']
        
        if action == 'create_faculty_user':
            status = create_new_faculty_account(first_name, last_name, email, password)
            if status:
                flash('New Faculty account created successfully!', 'success')
            else:
                flash('An error occured in creating the account', 'error')
            return redirect(url_for('admin.admin_landing')) 

        elif action == 'go_back':
            return render_template('admin_landing.html') 

@admin_bp.route('/create_etextbook')
def create_etextbook():
    pass

@admin_bp.route('/modify_etextbook')
def modify_etextbook():
    pass

@admin_bp.route('/create_active_course')
def create_active_course():
    pass

@admin_bp.route('/create_evaluation_course')
def create_evaluation_course():
    pass

  