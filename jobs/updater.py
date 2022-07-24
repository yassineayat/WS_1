import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger, timedelta

from .jobs import *


def start():
	scheduler = BackgroundScheduler()
	scheduler.start()
	trigger = CronTrigger(
			year="*", month="*", day="*", hour="2", minute="49", second="50"
		)
	trigger2 = CronTrigger(
		year="*", month="*", day="*", hour="0", minute="00", second="00"
	)
	scheduler.add_job(schedule_api, trigger=trigger)
	scheduler.add_job(ET0_calc, trigger=trigger2)
	scheduler.add_job(schedule_api2, 'interval', minutes=15)
	scheduler.print_jobs()
	# scheduler.pause()


