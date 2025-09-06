from flask import Flask

from blueprints.home import home_bp
from blueprints.reservation import reservation_bp
from blueprints.coupon import coupon_bp
from blueprints.info import info_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'

# Blueprint登録
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(reservation_bp, url_prefix='/reservation')
app.register_blueprint(coupon_bp, url_prefix='/coupon')
app.register_blueprint(info_bp, url_prefix='/info')

@app.route('/healthcheck')
def health_check():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
