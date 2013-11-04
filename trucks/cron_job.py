import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'trucks.settings'
from trucks import hipchat_posting
from trucks import event_persistance

def run_post_todays_minna_vendors():
    """
    Posts todays food trucks on Minna street
    To be called by a cron job (currently done by Heroku Scheduler)
    """
    hipchat_posting.post_todays_minna_vendors()

def run_store_last_30_days_vendors():
    """
    Stores data retrieved from facebook's event pages to database
    To be called by a cron job (currently done by Heroku Scheduler)
    """
    event_persistance.store_last_30_days_vendors()
