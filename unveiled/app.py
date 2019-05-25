"""
Main Application.
"""
from __future__ import absolute_import
from flask import jsonify, g, session, Flask, request, render_template
from werkzeug.utils import import_string
from unveiled.config import DEBUG, LOG_FORMAT
import logging
import unveiled.err_handlers as err_handlers

if DEBUG:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

api_blueprints = [
    'face_reco',
    'face_det'
]

def create_app():
    """ Create flask application. """
    app = Flask(__name__)
    app.config.from_object('unveiled.config')

    # Register blueprints
    for bp_name in api_blueprints:
        bp = import_string('%s.blueprints.%s:bp' % (__package__, bp_name))
        print('Registering bp: %s' % bp_name)
        app.register_blueprint(bp)

    @app.route('/')
    def index():
        """ Root handler. """
        return render_template('home.html', active_tab="tab1")

    # register error handlers
    app.register_error_handler(404, err_handlers.page_not_found)
    app.register_error_handler(403, err_handlers.page_forbidden)
    app.register_error_handler(500, err_handlers.internal_server_error)

    return app

if __name__ == '__main__':
    """ Main entrypoint. """
    logging.basicConfig(level=loglevel,
                        format=LOG_FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S %z')

    app = create_app()
    print('Created app.')