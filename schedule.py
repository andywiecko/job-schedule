#!/bin/python
# ======================================================================
__author__ = "andywiecko"
__version__ = "1.2"
# TODO
# - make some clean up
# + ... some defs
# + ... queue the jobs
# + hide remaining jobs in one function
# + handle errors
# - config with '.' in a name and autogenerating config with PID
# ======================================================================
import src.popenJobs as popen
from src.libs import *
# sync time in seconds
sync_time = 0.1
# file name with jobs
filename = 'jobs.txt'
# example:
"""
python schedule.py jobs.txt        # job will be load from jobs.txt ...
python schedule.py jobs.txt 0.1  # ...with sync time 0.1 sec
"""
# seting parameters via argv
if len(sys.argv)==2: 
    filename         = sys.argv[1]
if len(sys.argv)==3: 
    filename         = sys.argv[1]
    sync_time        = float(sys.argv[2])

# load file with jobs
popen.LoadJobs(filename)
# number of all jobs in queue
popen.all_jobs = len(popen.queue_jobs)
# jobs done counter
popen.done_jobs = 0
popen.SetErrorFile()
popen.importSettings('.config.py')
popen.reloadLib()
# ===================== INITIALIZATION WORKERS =========================
popen.InitWorkers()
# ===================== POPING JOBS FROM QUEUE =========================
print
tmp_max_running_jobs = popen.max_running_jobs
popen.SetGlobalTime()
popen.ResetTime()
popen.PrintDone()

while (popen.queue_jobs != [] or popen.running_jobs != []):
     time.sleep(sync_time)

     try:
          popen.reloadLib()
          error = ""
     except:
          error = "Syntax ERROR: there is an error in config.py file\n"
     tmp_max_running_jobs = popen.config.max_running_jobs

     # add missing workers
     if tmp_max_running_jobs > popen.max_running_jobs:
          popen.ResetTime()
          diff = tmp_max_running_jobs - popen.max_running_jobs
          if diff > len(popen.queue_jobs): diff = len(popen.queue_jobs)
          popen.AppendWorkersToJobs(diff)
          popen.max_running_jobs = tmp_max_running_jobs
          popen.PrintDone()

     for i in range(len(popen.running_jobs)):
          proc = popen.running_jobs[i]
          returnCode = proc.poll()
          if returnCode != None:

               if returnCode != 0:
                    popen.numErrors += 1

               if popen.queue_jobs == []: 
                    popen.running_jobs.remove(proc)
                    popen.doneOnTime += 1
                    popen.done_jobs += 1
                    break

               if tmp_max_running_jobs < popen.max_running_jobs:
                    popen.PopWorkerFromJobs(proc)                    
                    break
               else:
                    popen.PopJobFromQueue(i)

popen.PrintDone()
