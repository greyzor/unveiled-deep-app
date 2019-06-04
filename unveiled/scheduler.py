"""
Scheduled Periodic jobs.
"""
from flask import current_app as app
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import apscheduler

SCHEDULER = BackgroundScheduler()

def _refresh_apis(urls):
    """ Refresh list of apis registered in config, using default http/s GET"""
    for url in urls:
        print('[scheduler] refreshing: {}'.format(url))
        _ = requests.get(url)

def init_scheduled_jobs():
    """ Init scheduler to run period jobs.
    Should be called within flask app context.
    """
    global SCHEDULER

    print('[scheduler] adding_new_job: refresh apis !')
    print(SCHEDULER.get_jobs())

    job = SCHEDULER.add_job(
        _refresh_apis,
        'interval',
        minutes=app.config['REFRESH_PERIOD'],
        kwargs={
            'urls': app.config['REFRESH_URLS']
        }
    )
    SCHEDULER.start()