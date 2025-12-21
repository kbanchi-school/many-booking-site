from flask import render_template, request, redirect, url_for
from . import info_bp

from database import Notification

@info_bp.route('/')
def info():
    isread = request.args.get("is_read")

    query = Notification.select()

    if isread in ("0", "1"):
        query = query.where(Notification.is_read == int(isread))

    return render_template('info.html', notifications=query)


@info_bp.route('/read/<id>', methods=['POST'])
def info_read(id):
    notification = Notification.get(id=id)
    notification.is_read = 1
    notification.save()
    return redirect("/info/")