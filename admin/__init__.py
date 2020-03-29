from flask import Flask, current_app,  send_from_directory, redirect, url_for, escape, request, render_template, make_response
from flask_cors import *
from os import getcwd


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

    @app.route('/getlogfile')
    def getlogfile():
        directory = getcwd()  # 假设在当前目录
        filename = 'log.log'
        response = make_response(send_from_directory(directory + '/log/', filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
        return response

    CORS(app, supports_credentials=True)
    app.run(host="0.0.0.0", port=3080, debug=False)
