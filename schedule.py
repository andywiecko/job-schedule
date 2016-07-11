#!/bin/python
# ======================================================================
__author__ = "andywiecko"
__version__ = "1.0"
# ======================================================================
import os
import subprocess
import time
# ======================================================================
# ==================== PARAMETERS DEFINE BY USER =======================
# ======================================================================
# max number of jobs running at once
max_running_jobs = 8
# sync time in seconds
sync_time = 0.1
# file name with jobs
filename = 'jobs.txt'
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
# ======================================================================
# ===================== INITIALIZATION WORKERS =========================
# ======================================================================
for i in range(max_running_jobs):
    running_jobs.append(subprocess.Popen(queue_jobs.pop(), shell = True))
# ======================================================================
# ===================== POPING JOBS FROM QUEUE =========================
# ======================================================================
while (queue_jobs != []):
    time.sleep(sync_time)
    for i in range(max_running_jobs):
        proc = running_jobs[i]
        
        if proc.poll() == 0:
            if queue_jobs == []: break
            running_jobs[i] = subprocess.Popen(queue_jobs.pop(), shell = True)
            done_jobs += 1
            print 'jobs done: ',done_jobs,'/', all_jobs,' (workers: ',len(running_jobs),')'
# ======================================================================
# ====================== REMAINING LAST JOBS ===========================
# ======================================================================
while (running_jobs != []):
    time.sleep(sync_time)
    for proc in running_jobs:

        if proc.poll() == 0:
            running_jobs.remove(proc)
            done_jobs += 1
            print 'jobs done: ',done_jobs,'/', all_jobs,' (workers: ',len(running_jobs),')'
# ======================================================================
