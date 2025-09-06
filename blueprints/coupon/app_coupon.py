from flask import render_template, request, redirect, url_for
from . import coupon_bp

@coupon_bp.route('/')
def top():
    return render_template('coupon/top.html')