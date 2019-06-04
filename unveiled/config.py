""" Configuration variables """
DEBUG = True
LOG_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s @ %(lineno)s]: %(message)s'
UPLOAD_FOLDER = 'unveiled/static/images/' #'/tmp/'
BASEURL_REMOTE_WORKER_INCEPTION = 'https://unveiled-inception-worker-api.herokuapp.com'
REFRESH_URLS = [
	'https://unveiled-app.herokuapp.com/api/1/status',
	'https://unveiled-inception-worker-api.herokuapp.com/api/1/status'
]
REFRESH_PERIOD = 12 # minutes