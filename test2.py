
import random
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def handle_job(**kwargs):
    msg = "running job: " + kwargs['id'] + " interval: " + kwargs['interval']
    print(msg)
    time.sleep(5)


def main():
    jobstores = {
        'memory': MemoryJobStore()
    }
    executors = {
        'default': ProcessPoolExecutor(10),
        'threadpool': ThreadPoolExecutor(350)
    }
    job_defaults = {
        'max_instances': 10000
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    ''' Add jobs here '''
    x = 1
    for x in range(1, 3500):
        interval=random.randint(30, 120)
        scheduler.add_job(handle_job, 'interval', seconds=interval, kwargs={'id': str(x), 'interval': str(interval)})
        x += 1

    print("\nStarting Scheduler...")

    scheduler.start()

    while True:
        time.sleep(1)

    print("Scheduleder started")

    print("Shutting down... please wait!")

    scheduler.shutdown()


if __name__ == "__main__":
    main()