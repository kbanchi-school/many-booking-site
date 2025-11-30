from flask import render_template, request, redirect, url_for
from . import reservation_bp
from database import Reservation
from database import Salon
from database import Address

@reservation_bp.route('/')
def reservation():
    reservations = Reservation.select(Reservation,Salon,Address).join(Salon).join(Address)
    return render_template('reservation.html',reservations=reservations)