"""
Blueprint for face recoginition.
"""
from flask import Blueprint, render_template, abort
from jinja2.exceptions import TemplateNotFound
from unveiled.lib.utils import create_blueprint

bp = create_blueprint('face_reco', __name__, 'face_reco', is_api=False)

@bp.route('/')
def handle_face_recognition():
    """ Handler for blueprint's root. """
    try:
        return render_template('face_reco.html')
    except TemplateNotFound:
        abort(404)