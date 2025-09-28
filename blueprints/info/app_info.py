from flask import render_template, request, redirect, url_for
from . import info_bp

from database import Notification

@info_bp.route('/')
def info():
    notifications = Notification.select()
    return render_template('info.html', notifications=notifications)