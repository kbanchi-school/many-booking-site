from flask import render_template, request, redirect, url_for
from . import coupon_bp

from database import Coupon
from database import Coupon
from database import Salon
from database import Address


@coupon_bp.route('/')
def coupon():
    category = request.args.get("category","")
    
    print(category)
    if category == "use":
        coupons = Coupon.select(Coupon,Salon,Address).join(Salon).join(Address).where(Coupon. starts_at == 2)
    elif category == "uses":
        coupons = Coupon.select(Coupon,Salon,Address).join(Salon).join(Address).where(Coupon.ends_at == 1)
    elif category == "uses":
        coupons = Coupon.select(Coupon,Salon,Address).join(Salon).join(Address).where(Coupon.is_active == 3)
    else:
        coupons = Coupon.select(Coupon,Salon,Address).join(Salon).join(Address)
    return render_template('coupon.html', coupons=coupons)