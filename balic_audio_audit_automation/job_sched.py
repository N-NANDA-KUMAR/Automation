from time import sleep
from datetime import date, datetime
from balic_daily_audits import to_schedule_job
from apscheduler.schedulers.background import BackgroundScheduler


sched = BackgroundScheduler()

sched.add_job(to_schedule_job,"interval",seconds =20)
sched.start()

while True:
    sleep(1)