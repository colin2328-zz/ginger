from apscheduler.scheduler import Scheduler
import os
os.getcwd()
import facebook_scraper

sched = Scheduler()

@sched.interval_schedule(seconds=3)
def timed_job():
	print 'start job'
	
	# facebook_scraper.post_todays_minna_vendors()

# @sched.cron_schedule(day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print 'This job is run every weekday at 5pm.'

sched.start()

while True:
	pass