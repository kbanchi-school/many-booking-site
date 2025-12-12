from flask import render_template, request, redirect, url_for
from . import reservation_bp
from database import Reservation
from database import Salon
from database import Address

@reservation_bp.route('/')
def reservation():
    category = request.args.get("category","")
    print(category)
    if category == "reservation":
        reservations = Reservation.select(Reservation,Salon,Address).join(Salon).join(Address).where(Reservation.status == 2)
    elif category == "reservation history":
        reservations = Reservation.select(Reservation,Salon,Address).join(Salon).join(Address).where(Reservation.payment_status == 1)
    else:
        reservations = Reservation.select(Reservation,Salon,Address).join(Salon).join(Address)
    return render_template('reservation.html',reservations=reservations)