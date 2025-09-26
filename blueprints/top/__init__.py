from flask import Blueprint

top_bp = Blueprint('top', __name__)

from . import app_top