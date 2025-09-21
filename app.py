import os

from flask import Flask
from flask import render_template

from database import *

from dotenv import load_dotenv
load_dotenv()

# .env を読み込み
load_dotenv()
# 環境変数を取得
ENV = os.getenv("ENV")
LIFF_ID = os.getenv("LIFF_ID")
LINE_CHANNEL_ID = os.getenv("LINE_CHANNEL_ID")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

LIFF_ID = os.getenv("LIFF_ID")
ENV = os.getenv("ENV")

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/login')
def login():
    return render_template('login.html', liff_id=LIFF_ID, env=ENV)

@app.route('/db_work')
def db_work():
    persons = Person.select()
    return render_template('db_work.html', persons=persons)

@app.route('/kazunori')
def kazunori():
    return render_template('kazunori.html')

@app.route('/aoi')
def aoi():
    return render_template('aoi.html')

@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')

@app.route('/coupon')
def coupon():
    return render_template('coupon.html')

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
