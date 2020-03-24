from flask import Flask, current_app,  g, session, redirect, url_for, escape, request, render_template, make_response
from flask_cors import *


def start_admin(blueprints=[], services={}):
    app = Flask(__name__)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    with app.app_context():
        current_app.services = services

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    CORS(app, supports_credentials=True)
    app.run(host="127.0.0.1", port=3080, debug=False)
