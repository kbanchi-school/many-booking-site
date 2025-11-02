from datetime import datetime

from flask import render_template, request, redirect, url_for
from . import home_bp

from database import Salon , Service , Address ,WorkingHour

@home_bp.route('/')
def home():
    today_weekday = datetime.now().weekday()
    addresses = Address.select(Address, Salon, WorkingHour).join(Salon).join(WorkingHour).where(WorkingHour.weekday == today_weekday)
    return render_template('home.html', addresses=addresses)

@home_bp.route('/detail/<id>')
def detail(id):
    salon = Salon.get(Salon.id == id)
    services = Service.select().where(Service.salon == salon)
    workinghour = WorkingHour.get(WorkingHour.id == id)


    return render_template('home_detail.html', salon=salon, services=services)