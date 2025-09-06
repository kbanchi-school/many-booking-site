from flask import render_template, request, redirect, url_for
from . import auth_bp

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')
