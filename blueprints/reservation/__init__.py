from flask import Blueprint

reservation_bp = Blueprint('reservation', __name__)

from . import app_reservation