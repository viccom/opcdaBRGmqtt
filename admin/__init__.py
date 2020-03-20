from flask import Flask, current_app
from flask_cors import *


def start_admin(blueprints=[], services={}):
    app = Flask(__name__)
    with app.app_context():
        current_app.services = services

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route("/")
    def index():
        # resp = make_response(render_template(...))
        # resp.set_cookie('username', 'the username')
        # return resp
        # service = current_app.services.get('vspc_service')
        return "ThingsRoot Service bundle!!"

    CORS(app, supports_credentials=True)
    app.run(host="127.0.0.1", port=3080)
