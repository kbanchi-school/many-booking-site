from datetime import datetime
from peewee import prefetch, JOIN
from flask import render_template, request, redirect, url_for
from . import home_bp

from database import Salon , Service , Address ,WorkingHour

@home_bp.route('/')
def home():
    today_weekday = datetime.now().weekday()
    salons_q = (
        Salon
        .select(Salon, Address, WorkingHour)
        .join(Address)
        .switch(Salon)
        .join(WorkingHour)
        .where(
            WorkingHour.weekday == today_weekday
        )
    )
    services_q = (
        Service
        .select()
    )
    salons = prefetch(salons_q, services_q)
    return render_template('home.html', salons=salons)

@home_bp.route('/detail/<id>')
def detail(id):
    salon = Salon.get(Salon.id == id)
    services = Service.select().where(Service.salon == salon)
    workinghour = WorkingHour.get(WorkingHour.id == id)


    return render_template('home_detail.html', salon=salon, services=services ,workinghour=workinghour)