"""
Face Detection Blueprint.
"""
from flask import Blueprint, render_template, abort, redirect, request
from flask import current_app as app
from jinja2.exceptions import TemplateNotFound
from unveiled.lib.utils import create_blueprint
from unveiled.lib.utils import mkdir_p
from unveiled.services.face_det import find_face_locations
from unveiled.services.url_parser import extract_image_url
from unveiled.services.remote_worker import remote_classify_images

from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
import os
import uuid
import requests

CLASSIFIER_MIN_THRESH = 0.20 # confidence threshold, used to select final classes to show

bp = create_blueprint('face_det', __name__, 'face_det', is_api=False)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
QUERY_TERM_DEFAULT = "face"
RANDOM_IMAGES_BASE_URL = "https://source.unsplash.com/800x450/?"
REQ_TYPE_DEFAULT = 'q' # query


def allowed_file(filename):
    """ Is filename allowed. """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image_file_local(file, file_name, upload_folder, img_id=None):
    """ Helper to save image file locally """
    # Craft file name
    fname = secure_filename(file_name)
    img_id = img_id or uuid.uuid4().hex
    fname = 'tmp-{uid}-{fname}'.format(fname=fname, uid=img_id)

    # Save image file.
    mkdir_p(upload_folder)
    fpath = os.path.join(upload_folder, fname)
    print('Saving file to: %s' % fpath)
    file.save(fpath)

    file.stream.seek(0) # seek to the beginning of file

    return (file, fname)

def fetch_image_from_url(url_ext):
    """ Fetch an image from a given url. """
    print('Fetching images from external url: {url_ext}'.format(url_ext=url_ext))

    ## Check if there is we get a redirect
    r = requests.get(url_ext)
    print('url: %s' % r.url)

    input_html = None
    if r.url == url_ext: # no redirect
        input_html = r.text # no need to fetch the html content again
    else:
        url_ext = r.url # update url to redirected one.

    # Extract image from url.
    (top_img, _) = extract_image_url(url_ext, input_html=input_html)
    if not top_img:
        print('Assuming the redirected url points to the image..')
        top_img = url_ext

    print('GET remote file.. : %s' % top_img)
    r = requests.get(top_img)
    fpath = '/tmp/ext-{uid}'.format(uid=uuid.uuid4().hex)
    print('Saving to: {}'.format(fpath))
    with open(fpath, 'wb') as f:
        f.write(r.content)

    file_name = 'external.jpg' # FIXME
    print('Loading FileStorage() from: {}'.format(fpath))
    file = FileStorage(stream=open(fpath,'rb'), filename=file_name)
    os.remove(fpath)

    return (url_ext, file, file_name)


@bp.route('/', methods=['POST', 'GET'])
def handle_face_detection():
    """ Handler for blueprint's root. """
    global RANDOM_IMAGES_BASE_URL
    global QUERY_TERM_DEFAULT
    global REQ_TYPE_DEFAULT
    global CLASSIFIER

    face_results = {'face_locations': []} # face_results dict containing face_locations field.
    img_path = "#" # image url to be rendered in template, when no face detected.
    cropped_imgs = [] # cropped images urls to be rendered in template.
    img_path_final = "#" # image url to be rendered in template, when face detected.
    img_classes = {} # detected image classes dict: each key is class, value is confidence score.
    img_classification_error = False
    file = None # file stream
    file_name = None # file name to use for saving final image locally.
    active_tab = None # active tab
    query = "" # default value for query param
    url_ext = "" # default value for url_ext param
    req_type = REQ_TYPE_DEFAULT # type query by default

    # Check if a valid image file was uploaded
    if request.method == 'POST':

        # Get request type: either query, url or file.
        req_type = request.args.get('type', REQ_TYPE_DEFAULT)

        if req_type == 'q':
            # request type: query
            query = request.form.get('query', "")
            query = query or QUERY_TERM_DEFAULT
            query = query.split(' ')[0] # first term

            # overriding params
            url_ext = "{base_url}{query}".format(
                base_url=RANDOM_IMAGES_BASE_URL, query=query
            )

            # fetch image from url.
            (url_ext, file, file_name) = fetch_image_from_url(url_ext)

            # set active tab
            active_tab = "tab3"

        elif req_type == 'url':
            # request type: url
            url_ext = request.form.get('url_ext', "")

            # fetch image from url.
            if len(url_ext) > 0:
                (url_ext, file, file_name) = fetch_image_from_url(url_ext)

                # set active tab
                active_tab = active_tab or "tab2"

        elif req_type == 'f': # request type: file

            # no file provided, then redirect
            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']
            file_name = file.filename

            # file name empty, then redirect
            if file_name == '':
                return redirect(request.url)

            # set active tab
            active_tab = "tab1"

        else:
            raise Exception('Unsupported request type: %s' % req_type)

        ## At this point, we have downloaded a file locally.
        ## Lets process it and extract some nice features !
        if file and allowed_file(file_name):
            # Saving the file.
            upload_folder = app.config['UPLOAD_FOLDER']
            file, fname = save_image_file_local(file, file_name, upload_folder, img_id=None)

            # The image file seems valid! Detect faces and return the result.
            face_results = find_face_locations(file, out_dir=upload_folder)

            # Classify image contents, call remote worker.
            img_path = os.path.join(upload_folder, fname)
            res = remote_classify_images(img_path)
            print('remote inceptionv3 classification took: {} sec.'.format(res['timing']))
            img_classification_error = bool(res['status']!='done')
            res = res['results']

            # Filter classifications based on score threshold.
            img_classes = dict([(_t[1], float(_t[2]))
                for _t in filter(lambda t: float(t[2]) > CLASSIFIER_MIN_THRESH, res)
            ])
            print(img_classes)

            img_dir = '../static/images'
            img_path = os.path.join(img_dir, '{fname}'.format(fname=fname))
            cropped_imgs = [os.path.join(img_dir, src) for src in face_results['cropped_imgs']]
            img_path_final = os.path.join(img_dir, '{fname}'.format(fname=face_results['img_src']))

    if query: # either query, or url_ext
        url_ext = ""

    try:
        return render_template('face_det.html',
                                face_results=face_results,
                                img_path=img_path,
                                cropped_imgs=cropped_imgs,
                                img_path_final=img_path_final,
                                img_classes=img_classes,
                                img_classification_error=img_classification_error,
                                active_tab=active_tab,
                                query=query, # FIXME: frontend should handle its state.
                                url_ext=url_ext, # FIXME: frontend should handle its state.
                                ga_track_id=os.getenv('GA_TRACK_ID', '') # FIXME: inject from elsewhere.
                                )
    except TemplateNotFound:
        abort(404)