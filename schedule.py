#!/bin/python
# ======================================================================
__author__ = "andywiecko"
__version__ = "1.2"
# TODO
# - make some clean up
# - ... some defs
# - ... queue the jobs
# - hide remaining jobs in one function
# - handle errors
# - config with '.' in a name and autogenerating config with PID
# ======================================================================
import src.popenJobs as popen
from src.libs import *
#sys.stdout = open("file.txt", "rw+")
# sync time in seconds
sync_time = 0.1
# file name with jobs
filename = 'jobs.txt'
# example:
"""
python schedule.py jobs.txt        # job will be load from jobs.txt ...
python schedule.py jobs.txt 3      # ...with 3 workers
python schedule.py jobs.txt 3 0.1  # ...with sync time 0.1 sec
"""
# seting parameters via argv
if len(sys.argv)==2: 
    filename         = sys.argv[1]
if len(sys.argv)==3: 
    filename         = sys.argv[1]
    popen.max_running_jobs = int(sys.argv[2])
if len(sys.argv)==4:
    filename         = sys.argv[1]
    popen.max_running_jobs = int(sys.argv[2])
    sync_time        = float(sys.argv[3])

# load file with jobs
popen.LoadJobs(filename)
# number of all jobs in queue
popen.all_jobs = len(popen.queue_jobs)
# jobs done counter
popen.done_jobs = 0
import config
# ===================== INITIALIZATION WORKERS =========================
popen.InitWorkers()
# ===================== POPING JOBS FROM QUEUE =========================
print
tmp_max_running_jobs = popen.max_running_jobs
popen.ResetTime()
popen.PrintDone()
while (popen.queue_jobs != []):
     time.sleep(sync_time)

     try:
          reload(config)
          error = ""
     except:
          error = "Syntax ERROR: there is an error in config.py file\n" 
     tmp_max_running_jobs = config.max_running_jobs
     if tmp_max_running_jobs > popen.max_running_jobs:
          popen.ResetTime()
          diff = tmp_max_running_jobs - popen.max_running_jobs
          popen.AppendWorkersToJobs(diff)
          popen.max_running_jobs = tmp_max_running_jobs

     for i in range(popen.max_running_jobs):
          proc = popen.running_jobs[i]
          if proc.poll() != None:
               if popen.queue_jobs == []: break

               if tmp_max_running_jobs < popen.max_running_jobs:
                    popen.PopWorkerFromJobs(proc)                    
                    break
               else:
                    popen.PopJobFromQueue(i)

# ====================== REMAINING LAST JOBS ===========================
while (popen.running_jobs != []):
    time.sleep(sync_time)
    for proc in popen.running_jobs:
        if proc.poll() != None:
            popen.running_jobs.remove(proc)
            popen.done_jobs += 1
            print 'jobs done: ',popen.done_jobs,'/', popen.all_jobs,' (workers: ',len(popen.running_jobs),')'
