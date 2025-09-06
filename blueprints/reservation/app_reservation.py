from flask import render_template, request, redirect, url_for
from . import reservation_bp

@reservation_bp.route('/')
def top():
    return render_template('reservation/top.html')