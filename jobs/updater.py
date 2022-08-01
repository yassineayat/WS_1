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
		year="*", month="*", day="*", hour="0", minute="06", second="00"
	)
	trigger3 = CronTrigger(
		year="*", month="*", day="*", hour="13", minute="30", second="00"
	)
	scheduler.add_job(schedule_api, trigger=trigger)
	scheduler.add_job(ET0_calc, trigger=trigger2)
	scheduler.add_job(FWI, trigger=trigger3)
	scheduler.add_job(schedule_api2, 'interval', minutes=1,seconds=30)
	scheduler.add_job(schedule_api3, 'interval', seconds=30)
	# print("ok")

	scheduler.print_jobs()
	# scheduler.pause()


