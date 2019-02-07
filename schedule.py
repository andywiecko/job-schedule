#!/bin/python
# ======================================================================
__author__ = "andywiecko"
__version__ = "1.2"
# TODO
# - make some clean up
# - ... some defs
# - ... queue the jobs
# - hide remaining jobs in one function
# ======================================================================
import os
import subprocess
import time
import sys
# ======================================================================
# ==================== PARAMETERS DEFINE BY USER =======================
# ======================================================================
# max number of jobs running at once
max_running_jobs = 8
# sync time in seconds
sync_time = 0.1
# file name with jobs
filename = 'jobs.txt'
# seting parameters via argv
# example:
"""
python schedule.py jobs.txt        # job will be load from jobs.txt ...
python schedule.py jobs.txt 3      # ...with 3 workers
python schedule.py jobs.txt 3 0.1  # ...with sync time 0.1 sec
"""
if len(sys.argv)==2: 
    filename         = sys.argv[1]
if len(sys.argv)==3: 
    filename         = sys.argv[1]
    max_running_jobs = int(sys.argv[2])
if len(sys.argv)==4:
    filename         = sys.argv[1]
    max_running_jobs = int(sys.argv[2])
    sync_time        = float(sys.argv[3])
# ======================================================================
# ======================== PROGRAM CONSTANTS ===========================
# ======================================================================
# list with running jobs
running_jobs     = []
# stack with jobs in queue
queue_jobs       = []
# load file with jobs
queue_jobs = open(filename,'r').read().split('\n')[:-1]
# number of all jobs in queue
all_jobs = len(queue_jobs)
# jobs done counter
done_jobs = 0
import config
# ======================================================================
# ===================== INITIALIZATION WORKERS =========================
# ======================================================================
for i in range(all_jobs if max_running_jobs > all_jobs else max_running_jobs):
    running_jobs.append(subprocess.Popen(queue_jobs.pop(), shell = True))
# ======================================================================
# ===================== POPING JOBS FROM QUEUE =========================
# ======================================================================
from datetime import datetime

tmp_max_running_jobs = max_running_jobs
TIME = time.time()
doneOnTime = 0
while (queue_jobs != []):
     time.sleep(sync_time)

     try:
          reload(config)
          error = ""
     except:
          error = "Syntax ERROR: there is an error in config.py file\n" 
     tmp_max_running_jobs = config.max_running_jobs
     if tmp_max_running_jobs > max_running_jobs:
          TIME = time.time()
          doneOnTime = 0
          diff = tmp_max_running_jobs - max_running_jobs
          for j in range(diff):
               running_jobs.append(subprocess.Popen(queue_jobs.pop(), shell = True))
          max_running_jobs = tmp_max_running_jobs

     for i in range(max_running_jobs):
          proc = running_jobs[i]
          if proc.poll() != None:
               if queue_jobs == []: break

               if tmp_max_running_jobs < max_running_jobs:
                    TIME = time.time()
                    doneOnTime = 0
                    running_jobs.remove(proc)
                    max_running_jobs -= 1
                    break
                    
               else:
                    running_jobs[i] = subprocess.Popen(queue_jobs.pop(), shell = True)
                    done_jobs += 1
                    doneOnTime += 1
                    print 'jobs done: ',done_jobs,'/', all_jobs,' (workers: ',len(running_jobs),')'
                    deltaTIME = (time.time() - TIME) / doneOnTime
                    deltaTIME = deltaTIME*(all_jobs-done_jobs)
                    print datetime.fromtimestamp(time.time()+deltaTIME).strftime("%A, %B %d, %Y %I:%M:%S")

# ======================================================================
# ====================== REMAINING LAST JOBS ===========================
# ======================================================================
while (running_jobs != []):
    time.sleep(sync_time)
    for proc in running_jobs:
        if proc.poll() != None:
            running_jobs.remove(proc)
            done_jobs += 1
            print 'jobs done: ',done_jobs,'/', all_jobs,' (workers: ',len(running_jobs),')'
# ======================================================================
