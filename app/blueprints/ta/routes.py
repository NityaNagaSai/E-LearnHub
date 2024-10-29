from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import ta_bp

@ta_bp.route('/home')
def ta_landing():
    return render_template('ta_landing.html')
