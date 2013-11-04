print 'entered'
from django.conf import settings
settings.configure()
import trucks.hipchat_posting as hipchat_posting
import trucks.event_persistance as event_persistance

def run_post_todays_minna_vendors():
    """
    Posts todays food trucks on Minna street
    To be called by a cron job (currently done by Heroku Scheduler)
    """
    print 'started'
    try:
        hipchat_posting.post_todays_minna_vendors()
    except Exception as e:
        print e
    print 'ended'

def run_store_last_30_days_vendors():
    """
    Stores data retrieved from facebook's event pages to database
    To be called by a cron job (currently done by Heroku Scheduler)
    """
    event_persistance.store_last_30_days_vendors()
