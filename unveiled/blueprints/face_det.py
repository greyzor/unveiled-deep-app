"""
"""
from flask import Blueprint, render_template, abort, redirect, request
from flask import current_app as app
from jinja2.exceptions import TemplateNotFound
from unveiled.lib.utils import create_blueprint
from unveiled.lib.utils import mkdir_p
from unveiled.services.face_det import find_face_locations
from unveiled.services.url_parser import extract_image_url
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
import os
import uuid
import requests

bp = create_blueprint('face_det', __name__, 'face_det', is_api=False)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """ """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file_local(file, file_name, upload_folder, img_id=None):
    """ """
    # Craft file name
    fname = secure_filename(file_name)
    img_id = img_id or uuid.uuid4().hex
    fname = 'tmp-{fname}-{uid}.jpg'.format(fname=fname, uid=img_id)

    # Save to dir.
    mkdir_p(upload_folder)
    fpath = os.path.join(upload_folder, fname)
    print('Saving to: %s' % fpath)
    file.save(fpath)

    file.stream.seek(0) # seek to the beginning of file
    return (file, fname)


@bp.route('/', methods=['POST', 'GET'])
def show_infos():
    """ """
    results = None
    img_path = "#"
    cropped_imgs = []
    img_path_final = "#"
    file = None # file stream
    file_name = None
    active_tab = "tab1"

    # Check if a valid image file was uploaded
    if request.method == 'POST':

        url_ext = request.form.get('url_ext', None)

        if url_ext is not None and len(url_ext) > 0:
            print('Fetching images from external url: {url_ext}'.format(url_ext=url_ext))

            ## Check if there is we get a redirect
            r = requests.get(url_ext)
            print('url: %s' % r.url)

            input_html = None
            if r.url == url_ext: # no redirect
                input_html = r.text # no need to fetch the html content again
            else:
                url_ext = r.url # update url to redirected one.

            (top_img, _) = extract_image_url(url_ext, input_html=input_html)
            if not top_img:
                print('Assuming the redirected url points to the image..')
                top_img = url_ext

            file_name = 'external.jpg' # FIXME

            print('Opening remote file.. : %s' % top_img)
            r = requests.get(top_img)
            fpath = '/tmp/ext-{uid}'.format(uid=uuid.uuid4().hex)
            with open(fpath, 'wb') as f:
                f.write(r.content)

            file = FileStorage(stream=open(fpath,'rb'), filename=file_name)
            os.remove(fpath)

            active_tab = "tab2"

        else:
            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']
            file_name = file.filename

            if file_name == '':
                return redirect(request.url)

            active_tab = "tab1"

        if file and allowed_file(file_name):
            # Saving the file.
            upload_folder = app.config['UPLOAD_FOLDER']
            file, fname = save_file_local(file, file_name, upload_folder, img_id=None) # random part in fname

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
                                img_path_final=img_path_final,
                                active_tab=active_tab)
    except TemplateNotFound:
        abort(404)