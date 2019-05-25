"""
Some helpers.
"""
from flask import Blueprint, jsonify, url_for, redirect, g, current_app, abort, request
from functools import partial, wraps
import os
import errno

ERROR_CODES = [400, 401, 403, 404, 408]

# from unveiled.libs.jsonutils import jsonize

# def patch_blueprint_route(bp):
#     origin_route = bp.route

#     def patched_route(self, rule, **options):
#         def decorator(f):
#             origin_route(rule, **options)(jsonize(f))
#         return decorator

#     bp.route = partial(patched_route, bp)

def create_blueprint(name, import_name, url_prefix=None, handle_http_error=True, is_api=False):
    """ Wrapper for blueprint creation.

    :param name: blueprint's name
    :param import_name: name of the package or module that this app belongs to.
    :param url_prefix: url prefix used for all URLs defined on the blueprint.
    :param handle_http_error: invoke handler when http error code encountered.
    :param is_api: is the blueprint an api.

    :returns: the blueprint.
    :rtype: flask.Blueprint
    """
    if url_prefix and url_prefix.startswith('/'):
        raise URLPrefixError('url_prefix ("%s") must not start with /' % url_prefix)

    bp_url_prefix = '/'
    if url_prefix:
        if is_api is True:
            bp_url_prefix = '/api/'

        bp_url_prefix = os.path.join(bp_url_prefix, url_prefix)

    bp = Blueprint(name, import_name, url_prefix=bp_url_prefix)

    if handle_http_error is True:

        def _error_hanlder(error):
            return jsonify({'error': error.description}), error.code

        for code in ERROR_CODES:
            bp.errorhandler(code)(_error_hanlder)

    # if jsonize is True:
    #     patch_blueprint_route(bp)

    return bp

def mkdir_p(_dir):
    """ Create recursive directory. """
    try:
        os.makedirs(_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise