"""
"""
from flask import jsonify, g, session, Flask, request, render_template
from werkzeug.utils import import_string
from unveiled.config import DEBUG, LOG_FORMAT
import logging

if DEBUG:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

api_blueprints = [
    'face_reco',
    'face_det'
]

def create_app():
    app = Flask(__name__)
    app.config.from_object('unveiled.config')

    for bp_name in api_blueprints:
        bp = import_string('%s.blueprints.%s:bp' % (__package__, bp_name))
        print('Registering bp: %s' % bp_name)
        app.register_blueprint(bp)

    @app.route('/')
    def index():
        """ """
        return render_template('home.html', active_tab="tab1")

    return app

if __name__ == '__main__':
    """ """
    logging.basicConfig(level=loglevel,
                        format=LOG_FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S %z')
    app = create_app()
    print('Created app.')