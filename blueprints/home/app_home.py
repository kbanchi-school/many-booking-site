from datetime import datetime
from peewee import prefetch, JOIN 
from flask import render_template, request, redirect, url_for
from . import home_bp

from database import Salon , Service , Address ,WorkingHour ,SalonImage

@home_bp.route('/')
def home():
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    print(search)
    today_weekday = datetime.now().weekday()
    salons_q = (
        Salon
        .select(Salon, Address, WorkingHour,SalonImage)
        .join(SalonImage)
        .switch(Salon)
        .join(Address)
        .switch(Salon)
        .join(WorkingHour)


        .where(
            (WorkingHour.weekday == today_weekday)&
            (SalonImage.sort_order == 0)&
            (
                (Salon.name.contains(search)) |
                (Salon.description.contains(search))
            )
            )
        )
    
    services_q = (
        Service
        .select()

        .where(
            (Service.name == category)
            )


    )
    salons = prefetch(salons_q, services_q)
    return render_template('home.html', salons=salons)

@home_bp.route('/detail/<id>')
def detail(id):
    salon = Salon.get(Salon.id == id)
    services = Service.select().where(Service.salon == salon)
    workinghour = WorkingHour.get(WorkingHour.id == id)

    return render_template('home_detail.html', salon=salon, services=services ,workinghour=workinghour)

@home_bp.route('/detail/<salon_id>/<service_id>/calendar')
def detail_calender(salon_id, service_id):
    salon = Salon.get(Salon.id == salon_id)
    service = Service.select().where(Service.id == service_id ,Service.salon == salon)
    workinghour = WorkingHour.get(WorkingHour.id == salon)

    return render_template('home_calendar.html',salon=salon, services=service ,workinghour=workinghour)