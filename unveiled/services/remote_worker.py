"""
"""
from flask import current_app as app
import requests
import os
import json
import traceback

EMPTY_RESULTS = {
    "status": "error",
    "timing": -1.,
    "results": []
}

REQUEST_TIMEOUT = 10.0 # seconds

def remote_classify_images(img_path):
    """ Call remote inceptionv3 worker.

    :param img_path: local path of image to be sent as request data.
    :type img_path: str
    :returns: classification results
    :rtype: dict{'status':str,'timing':float,'results':list}
    """
    global EMPTY_RESULTS
    global REQUEST_TIMEOUT

    img = open(img_path, 'rb').read()
    url = os.path.join(
        app.config['BASEURL_REMOTE_WORKER_INCEPTION'],
        'api/1/classify'
    )
    # call the remote service
    try:
        res = requests.post(url, data=img, timeout=REQUEST_TIMEOUT)
    except (requests.Timeout, requests.ConnectionError):
        return EMPTY_RESULTS

    # convert results to json
    try:
        data = res.json()
    except json.decoder.JSONDecodeError as e:
        print('[error]{}\n{}'.format(traceback.format_exc(),e))
        return EMPTY_RESULTS
    return data