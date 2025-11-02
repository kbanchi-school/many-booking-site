from flask import render_template, request, redirect, url_for
from . import coupon_bp

from database import Coupon

@coupon_bp.route('/')
def coupon():
    coupons = Coupon.select()
    return render_template('coupon.html', coupons=coupons)