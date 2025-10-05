from flask import render_template, request, redirect, url_for
from . import home_bp

from database import Salon

@home_bp.route('/')
def home():
    salons = Salon.select()
    return render_template('home.html', salons=salons)

@home_bp.route('/detail/<id>')
def detail(id):
    salon = Salon.get(Salon.id == id)
    return render_template('home_detail.html', salon=salon)