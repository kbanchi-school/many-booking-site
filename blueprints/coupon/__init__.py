from flask import Blueprint

coupon_bp = Blueprint('coupon', __name__)

from . import app_coupon