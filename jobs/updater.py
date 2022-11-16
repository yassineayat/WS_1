import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger, timedelta

from .jobs import *


def start():
	scheduler = BackgroundScheduler()
	scheduler.start()
	TEST = CronTrigger(
			year="*", month="*", day="*", hour="2", minute="49", second="50"
		)
	E = CronTrigger(
		year="*", month="*", day="*", hour="01", minute="00", second="00"
	)
	ET0 = CronTrigger(
		year="*", month="*", day="*", hour="01", minute="00", second="10"
	)
	FWIC = CronTrigger(
		year="*", month="*", day="*", hour="13", minute="30", second="00"
	)


	scheduler.add_job(schedule_api, trigger=TEST)
	scheduler.add_job(ET0_calc, trigger=E)
	scheduler.add_job(FWI, trigger=FWIC)
	scheduler.add_job(ET0o_calc, trigger=ET0)
	scheduler.add_job(schedule_api2, 'interval', minutes=1,seconds=30)
	scheduler.add_job(schedule_api3, 'interval', seconds=30)
	scheduler.add_job(evp, 'interval', seconds=30)

	# print("ok")

	scheduler.print_jobs()
	# scheduler.pause()


