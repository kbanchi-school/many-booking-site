import os

from flask import Flask
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from flask import jsonify
from flask import current_app

import requests


from datetime import timedelta

from database import *

from dotenv import load_dotenv
load_dotenv()

# .env を読み込み
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False  # 本番は True + HTTPS
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

    # 環境 & LIFF
    app.config["ENV"] = os.getenv("ENV")
    app.config["LIFF_ID"] = os.getenv("LIFF_ID")
    app.config["LINE_CHANNEL_ID"] = os.getenv("LINE_CHANNEL_ID")
    app.config["LINE_CHANNEL_SECRET"] = os.getenv("LINE_CHANNEL_SECRET")
    app.config["LINE_CHANNEL_ACCESS_TOKEN"] = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # テンプレ共通変数: current_user を常に使えるように
    @app.context_processor
    def inject_current_user():
        user = {
            "line_id": session.get("line_id"),
            "line_name": session.get("line_name"),
            "line_picture": session.get("line_picture"),
            "is_authenticated": bool(session.get("line_id")),
        }
        return dict(current_user=user)

    @app.route('/')
    def index():
        if not session.get("line_id"):
            return redirect("/login")
        return redirect("/top")

    @app.route('/login')
    def login():
        LIFF_ID = app.config["LIFF_ID"]
        ENV = app.config["ENV"]
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
    
    @app.route("/liff-login", methods=["POST"])
    def liff_login():
        """
        フロントから送られた id_token を LINE に検証依頼し、
        正当なら Flask セッションにユーザ情報を保存する。
        """
        data = request.get_json(silent=True) or {}
        id_token = data.get("id_token")
        profile_hint = data.get("profile")  # 参考用（サーバ側では信用しない）

        if not id_token:
            return jsonify({"ok": False, "error": "no id_token"}), 400

        # LINE IDトークン検証API
        # https://api.line.me/oauth2/v2.1/verify
        if current_app.config["ENV"] != "local":
            resp = requests.post(
                    "https://api.line.me/oauth2/v2.1/verify",
                    data={
                        "id_token": id_token,
                        "client_id": current_app.config["LINE_CHANNEL_ID"],
                    },
                    timeout=5,
                )
            if resp.status_code != 200:
                return jsonify({"ok": False, "error": "verify_failed", "detail": resp.text}), 400
            payload = resp.json()
            # payload 例: {"iss": "...", "sub": "Uxxxxxxxx", "name": "...", "picture": "...", ...}

            # セッションへ保存（ここだけを信頼ソースにする）
            session.permanent = True
            session["line_id"] = payload.get("sub")                 # ユーザID（必須）
            session["line_name"] = payload.get("name") or (profile_hint or {}).get("displayName")
            session["line_picture"] = payload.get("picture") or (profile_hint or {}).get("pictureUrl")
        else:
            session["line_id"] = profile_hint.get("userId")
            session["line_name"] = profile_hint.get("displayName")
            session["line_picture"] = profile_hint.get("pictureUrl")

        return jsonify({"ok": True, "user": {
            "line_id": session["line_id"],
            "line_name": session.get("line_name"),
            "line_picture": session.get("line_picture"),
        }})

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return jsonify({"ok": True})
    
    return app

if __name__ == '__main__':
    app = create_app()
    if app.config["ENV"] == "local" or app.config["ENV"] == "dev":
        app.run(debug=True, host='0.0.0.0', port=5001, ssl_context=("ssl/localhost+2.pem", "ssl/localhost+2-key.pem"))
    else:
        app.run(debug=True, host='0.0.0.0', port=5001)
