"""
Scheduled Periodic jobs.
"""
from flask import current_app as app
from apscheduler.schedulers.background import BackgroundScheduler
import requests

def _refresh_apis(urls):
    """ Refresh list of apis registered in config, using default http/s GET"""
    for url in urls:
        print('[scheduler] refreshing: {}'.format(url))
        _ = requests.get(url)

def init_scheduled_jobs():
    """ Init scheduler to run period jobs.
    Should be called within flask app context.

    :returns: scheduler object
    """
    print('[scheduler] adding_new_job: refresh apis !')
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(
        _refresh_apis,
        'interval',
        minutes=app.config['REFRESH_PERIOD'],
        kwargs={
            'urls': app.config['REFRESH_URLS']
        }
    )
    scheduler.start()
    return scheduler