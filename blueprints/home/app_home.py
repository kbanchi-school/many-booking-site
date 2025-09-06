from flask import render_template, request, redirect, url_for
from . import home_bp

@home_bp.route('/')
def top():
    return render_template('home/top.html')