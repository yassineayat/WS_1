from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler


def print_hello():
   print("time-->",datetime.datetime.now())
   print("hello")

def print_world():
   print("time-->",datetime.datetime.now())
   print("hello")


scheduler = BackgroundScheduler()
scheduler1 = BackgroundScheduler()