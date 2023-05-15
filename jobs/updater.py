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
	et = CronTrigger(
		year="*", month="*", day="*", hour="1", minute="05", second="30"
	)
	ETo0 = CronTrigger(
		year="*", month="*", day="*", hour="00", minute="25", second="00"
	)
	FWIC = CronTrigger(
		year="*", month="*", day="*", hour="13", minute="30", second="00"
	)


	scheduler.add_job(schedule_api, trigger=TEST)
	# scheduler.add_job(ET0_calc, trigger=et)
	scheduler.add_job(FWI, trigger=FWIC)
	#scheduler.add_job(ET0o_calc, trigger=ETo0)
	#scheduler.add_job(schedule_api2, 'interval', minutes=1,seconds=30)
	#scheduler.add_job(schedule_api3, 'interval', seconds=30)
	#scheduler.add_job(evp, 'interval', seconds=30)

	# print("ok")

	scheduler.print_jobs()
	# scheduler.pause()


