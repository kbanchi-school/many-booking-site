from flask import Blueprint

info_bp = Blueprint('info', __name__)

from . import app_info