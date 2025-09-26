from flask import render_template, request, redirect, url_for
from . import info_bp

@info_bp.route('/')
def info():
    return render_template('info.html')