#!/bin/python
from datetime import datetime
import sys
import time
import subprocess
# ======================================================================
# ======================== PROGRAM CONSTANTS ===========================
# ======================================================================
# max number of jobs running at once
max_running_jobs = 8
# list with running jobs
running_jobs     = []
# stack with jobs in queue
queue_jobs       = []
all_jobs = 0

done_jobs = 0

TIME = 0
doneOnTime = 0

def LoadJobs(filename):
    global queue_jobs
    queue_jobs = open(filename,'r').read().split('\n')[:-1]

def InitWorkers():
    global running_jobs,queue_jobs
    for i in range(all_jobs if max_running_jobs > all_jobs else max_running_jobs):
        running_jobs.append(subprocess.Popen(queue_jobs.pop(), shell = True))

def ResetTime():
     global TIME,doneOnTime
     TIME = time.time()
     doneOnTime = 0

BACK_TO_PREVLINE = "\033[F"
CLEAR_LINE = "\033[K"
def PrintDone():
#     print BACK_TO_PREVLINE,CLEAR_LINE,
     print BACK_TO_PREVLINE,CLEAR_LINE,
     
     print '\rjobs done: ',done_jobs,'/', all_jobs,' (workers: ',len(running_jobs),')'
     if doneOnTime != 0:
         deltaTIME = (time.time() - TIME) / doneOnTime
         deltaTIME = deltaTIME*(all_jobs-done_jobs)
         print 'Estimated time:',datetime.fromtimestamp(time.time()+deltaTIME).strftime("%A, %B %d, %Y %H:%M:%S"),
     else: print 'Estimating time ...',
     sys.stdout.flush()

def PopJobFromQueue(i):
     global done_jobs,doneOnTime,running_jobs,queue_jobs
     running_jobs[i] = subprocess.Popen(queue_jobs.pop(), shell = True)
     done_jobs += 1
     doneOnTime += 1
     PrintDone() 

def PopWorkerFromJobs(proc):
    global max_running_jobs,running_jobs
    ResetTime()
    running_jobs.remove(proc)
    max_running_jobs -= 1

def AppendWorkersToJobs(howMany):
    global running_jobs,queue_jobs
    for j in range(howMany):
         running_jobs.append(subprocess.Popen(queue_jobs.pop(), shell = True))

