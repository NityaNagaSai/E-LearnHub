from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import admin_bp
import mysql.connector
from mysql.connector import errorcode



@admin_bp.route('/home')
def admin_landing():
    return render_template('admin_landing.py')
  