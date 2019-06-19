"""
Scheduled Periodic jobs.
"""
from flask import current_app as app
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import apscheduler
import datetime

SCHEDULER = BackgroundScheduler()

def _should_refresh():
    """ Return True if we're allowed to refresh according to refresh interval. """
    (start_time, end_time) = app.config['REFRESH_INTERVAL']
    now = datetime.datetime.utcnow()

    start_offset = start_time.hour*60 + start_time.minute
    end_offset = end_time.hour*60 + end_time.minute
    cur_offset = now.hour*60 + now.minute

    # no refresh when outside from refresh interval boundaries
    return bool(cur_offset >= start_offset and cur_offset <= end_offset)

def _refresh_apis(urls):
    """ Refresh list of apis registered in config, using default http/s GET"""
    if not _should_refresh():
        return

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