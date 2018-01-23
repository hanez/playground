#!/usr/bin/python3 -tt

"""
Copyright (c) 2015 Johannes Findeisen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import logging
import logging.handlers
import os
import os.path as path
import random
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

__version__ = "0.1"

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Descriptiom of the program.",
        epilog="Some longer description",
        prog="test.py")

    parser.add_argument("--version", action="version", version="%(prog)s " + str(__version__))

    parser.add_argument("config", metavar="CONFIGFILE",
                        help="the configfile to use")

    parser.add_argument("-n", "--nocolor",
                        help="disable colored output")

    parser.add_argument("-l", "--logfile", default="./log/program.log", metavar="FILE",
                        help="set logfile to use (default: ./log/program.log)")

    parser.add_argument("-c", "--logcount", default=5, type=int,
                        help="maximum number of logfiles in rotation (default: 5)")

    parser.add_argument("-m", "--logsize", default=104857600000, type=int,
                        help="maximum logfile size in bytes (default: 10485760)")

    parser.add_argument("-t", "--threads", default=1000, type=int,
                        help="maximum number of scheduler threads (default: 3500)")

    parser.add_argument("-p", "--processes", default=100, type=int,
                        help="number of scheduler processes (default: 0)")

    output = parser.add_mutually_exclusive_group()
    output.add_argument("-q", "--quiet", action="store_const", dest="loglevel", const=logging.ERROR,
                        help="output only errors")

    output.add_argument("-w", "--warning", action="store_const", dest="loglevel", const=logging.WARNING,
                        help="output warnings")

    output.add_argument("-v", "--verbose", action="store_const", dest="loglevel", const=logging.INFO,
                        help="output info messages")

    output.add_argument("-d", "--debug", action="store_const", dest="loglevel", const=logging.DEBUG,
                        help="output debug messages")
    output.set_defaults(loglevel=logging.INFO)
    return parser.parse_args()


def handle_job(**kwargs):
    msg = "running job: " + kwargs['id'] + " interval: " + kwargs['interval']
    print(msg)
    logger.info(msg)
    for i in range(10):
        os.urandom(100)

    time.sleep(5)
    logger.info(msg + " FINISHED!")
    #print(kwargs)
    #for key, value in kwargs
    #logger.info("handle_job called")
    #time.sleep(random.randint(1, 59))
    #logger.info(kwargs)


def main():
    args = parse_args()

    print(args)

    logfile = path.expanduser(args.logfile)
    if not path.exists(path.dirname(logfile)):
        os.makedirs(path.dirname(logfile))

    root_logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    handler = logging.handlers.RotatingFileHandler(args.logfile, maxBytes=args.logsize, backupCount=args.logcount)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(args.loglevel)

    jobstores = {
        'memory': MemoryJobStore()
    }
    executors = {
        'default': ProcessPoolExecutor(args.processes),
        'threadpool': ThreadPoolExecutor(args.threads)
    }
    job_defaults = {
        'max_instances': 10000
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    ''' Add jobs here '''
    x = 1
    for x in range(1, 10000):
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
    logging.shutdown()


if __name__ == "__main__":
    main()