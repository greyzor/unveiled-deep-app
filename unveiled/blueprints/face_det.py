"""
"""
from flask import Blueprint, render_template, abort, redirect, request
from flask import current_app as app
from jinja2.exceptions import TemplateNotFound
from unveiled.lib.utils import create_blueprint
from unveiled.lib.utils import mkdir_p
from unveiled.services.face_det import find_face_locations
from werkzeug import secure_filename
import os
import uuid

bp = create_blueprint('face_det', __name__, 'face_det', is_api=False)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """ """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['POST', 'GET'])
def show_infos():
    """ """
    results = None
    img_path = "#"

    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Saving the file.
            fname = secure_filename(file.filename)
            img_id = uuid.uuid4().hex
            fname = 'tmp-{fname}-{uid}.jpg'.format(fname=fname, uid=img_id)
            upload_folder = app.config['UPLOAD_FOLDER']
            mkdir_p(upload_folder)
            fpath = os.path.join(upload_folder, fname)
            file.save(fpath)
            file.stream.seek(0) # seek to the beginning of file

            # The image file seems valid! Detect faces and return the result.
            results = find_face_locations(file, out_dir=upload_folder)

            # fpath = '/face_det/unveiled/static/images/avatar.jpg'
            img_dir = '../static/images'

            img_path = os.path.join(img_dir, '{fname}'.format(fname=fname))
            cropped_imgs = [os.path.join(img_dir, src) for src in results['cropped_imgs']]
            img_path_final = os.path.join(img_dir, '{fname}'.format(fname=results['img_src']))

    try:
        return render_template('face_det.html',
                                results=results,
                                img_path=img_path,
                                cropped_imgs=cropped_imgs,
                                img_path_final=img_path_final)
    except TemplateNotFound:
        abort(404)