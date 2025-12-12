from flask import render_template, request, redirect, url_for
from . import info_bp

from database import Notification

@info_bp.route('/')
def info():
    notifications = Notification.select()
    return render_template('info.html', notifications=notifications)

@info_bp.route('/read/<id>', methods=['POST'])
def info_read(id):
    notification = Notification.get(id=id)
    notification.is_read = 1
    notification.save()
    return redirect("/info/")