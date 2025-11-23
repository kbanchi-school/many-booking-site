from flask import render_template, request, redirect, url_for
from . import reservation_bp
from database import Reservation

@reservation_bp.route('/')
def reservation():
    reservations = Reservation.select()
    return render_template('reservation.html',reservations=reservations)