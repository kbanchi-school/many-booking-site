import os

from dotenv import load_dotenv
load_dotenv()

from flask import render_template, request, redirect, url_for
from . import auth_bp

LIFF_ID = os.getenv("LIFF_ID")
ENV = os.getenv("ENV")

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html', liff_id=LIFF_ID, env=ENV)
