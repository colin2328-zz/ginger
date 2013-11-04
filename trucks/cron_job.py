import trucks.facebook_scraper as facebook_scraper

def run_post_todays_minna_vendors():
    """
    Posts todays food trucks on Minna street
    To be called by a cron job (currently done by Heroku Scheduler)
    """
    print 'ran job'
    facebook_scraper.post_todays_minna_vendors()

# def scheduled_job():
#     print 'This job is run every weekday at 5pm.'
