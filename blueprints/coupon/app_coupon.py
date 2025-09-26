from flask import render_template, request, redirect, url_for
from . import coupon_bp

@coupon_bp.route('/')
def coupon():
    return render_template('coupon.html')