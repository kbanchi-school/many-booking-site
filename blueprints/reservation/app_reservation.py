from flask import render_template, request, redirect, url_for
from . import reservation_bp
from database import Reservation
from database import Salon

@reservation_bp.route('/')
def reservation():
    reservations = Reservation.select(Reservation,Salon).join(Salon)
    return render_template('reservation.html',reservations=reservations)