from flask import render_template, request, redirect, url_for
from . import home_bp

from database import Salon , Service , Address ,WorkingHour

@home_bp.route('/')
def home():
    salons = Salon.select()
    address = Address.select()
    workinghours = WorkingHour.select()
    return render_template('home.html', salons=salons, address=address, workinghours=workinghours)

@home_bp.route('/detail/<id>')
def detail(id):
    salon = Salon.get(Salon.id == id)
    services = Service.select().where(Service.salon == salon)


    return render_template('home_detail.html', salon=salon, services=services)