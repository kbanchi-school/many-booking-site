from flask import render_template, request, redirect, url_for
from . import info_bp

@info_bp.route('/')
def top():
    return render_template('info/top.html')