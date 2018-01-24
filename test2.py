import random
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def handle_job(**kwargs):
    msg = "running job: " + kwargs['id'] + " interval: " + kwargs['interval']
    print(msg)
    time.sleep(59)
    print(msg + " > finished!")


if __name__ == "__main__":
    jobstores = {
        'memory': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor(350),
        'processpool': ProcessPoolExecutor(10)
    }
    job_defaults = {
        'max_instances': 250
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    x = 1
    for x in range(1, 12000):
        interval=random.randint(60, 300)
        scheduler.add_job(handle_job, 'interval', seconds=interval, kwargs={'id': str(x), 'interval': str(interval)})
        x += 1

    scheduler.start()

    while True:
        time.sleep(1)

    scheduler.shutdown()
