"""
"""
from flask import Blueprint, jsonify, url_for, redirect, g, current_app, abort, request
from functools import partial, wraps
import os
import errno

ERROR_CODES = [400, 401, 403, 404, 408]

def create_blueprint(name, import_name, url_prefix=None, jsonize=True, handle_http_error=True, is_api=False):
    """ """
    if url_prefix and url_prefix.startswith('/'):
        raise URLPrefixError('url_prefix ("%s") must not start with /' % url_prefix)

    bp_url_prefix = '/'
    if url_prefix:
        if is_api is True:
            bp_url_prefix = '/api/'

        bp_url_prefix = os.path.join(bp_url_prefix, url_prefix)

    bp = Blueprint(name, import_name, url_prefix=bp_url_prefix)

    if handle_http_error:

        def _error_hanlder(error):
            return jsonify({'error': error.description}), error.code

        for code in ERROR_CODES:
            bp.errorhandler(code)(_error_hanlder)

    return bp

def mkdir_p(_dir):
    """ """
    try:
        os.makedirs(_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise