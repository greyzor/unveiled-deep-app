"""
"""
from flask import current_app as app
import requests
import os

def remote_classify_images(img_path):
    """ """
    img = open(img_path, 'rb').read()
    url = os.path.join(
        app.config['BASEURL_REMOTE_WORKER_INCEPTION'],
        'api/1/classify'
    )
    res = requests.post(url, data=img).json()
    return res