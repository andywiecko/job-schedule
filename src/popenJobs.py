#!/bin/python
from datetime import datetime
import sys
import time
import subprocess
import imp
# ======================================================================
# ======================== PROGRAM CONSTANTS ===========================
# ======================================================================
# max number of jobs running at once
max_running_jobs = 1
# list with running jobs
running_jobs     = []
# stack with jobs in queue
queue_jobs       = []
all_jobs = 0

done_jobs = 0

GLOBALTIME = 0
TIME = 0
doneOnTime = 0

numErrors = 0

output = ''

# status file
statusFile = '.status'
statusFILE = ''

# error file
errorFile = '.errors'
errorFILE = ''

# ======================================================================
# ======================== PROGRAM FUNCTIONS ===========================
# ======================================================================
def SetErrorFile():
    global errorFILE,errorFile
    errorFILE = open(errorFile,'w')


def LoadJobs(filename):
    global queue_jobs
    queue_jobs = open(filename,'r').read().split('\n')[:-1]

def InitWorkers():
    global running_jobs,queue_jobs
    for i in range(all_jobs if max_running_jobs > all_jobs else max_running_jobs):
        running_jobs.append(subprocess.Popen(queue_jobs.pop(), stderr=errorFILE, shell = True))

def SetGlobalTime():
     global GLOBALTIME
     GLOBALTIME = time.time()

def ResetTime():
     global TIME,doneOnTime
     TIME = time.time()
     doneOnTime = 0

BACK_TO_PREVLINE = "\033[F"
CLEAR_LINE = "\033[K"
thirdLine = 0

def ConvertToDHMS(time):
     days    = divmod(time, 86400)   
     hours   = divmod(days[1], 3600) 
     minutes = divmod(hours[1], 60)  
     seconds = divmod(minutes[1], 1) 
     return '%d days, %d hours, %d minutes and %d seconds' % (days[0], hours[0], minutes[0], seconds[0])

def JobsDone():
     return 'Jobs done: '+str(done_jobs)+' / '+str(all_jobs)+' (workers: '+str(len(running_jobs))+')\n'

def TotalComputationTime():
     GLTIME = time.time() - GLOBALTIME
     sys.stdout.write("\033[K")
     return 'Total computation time: '+ConvertToDHMS(GLTIME)

def EstimatingTime():
     return 'Estimating time ...'

def EstimatedTime():
     deltaTIME = (time.time() - TIME) / doneOnTime
     deltaTIME = deltaTIME*(all_jobs-done_jobs)
     return 'Estimated time: '+datetime.fromtimestamp(time.time()+deltaTIME).strftime("%A, %B %d, %Y %H:%M:%S")

def OccuredErrors():
     return '\nOccured errors: '+str(numErrors)+' (see log: '+errorFile+')'

def SaveStatus():
     global statusFILE 
     statusFILE = open(statusFile,'w')
     statusFILE.write(output)
     statusFILE.close()

def ClearLines():
     global thirdLine 
     if numErrors>0: 
         if thirdLine==0: 
             print
             thirdLine += 1
         print BACK_TO_PREVLINE,CLEAR_LINE,
     print BACK_TO_PREVLINE,CLEAR_LINE,'\r',
  
def PrintDone():
     global thirdLine,output
     ClearLines()
     output = ''
     output += JobsDone()
     if done_jobs ==0:                             output+= EstimatingTime()
     if done_jobs == all_jobs:                     output+= TotalComputationTime()
     if doneOnTime != 0 and done_jobs != all_jobs: output+= EstimatedTime()
     if numErrors > 0:                             output+= OccuredErrors()
    
     print output,
     SaveStatus()
     sys.stdout.flush()

def PopJobFromQueue(i):
     global done_jobs,doneOnTime,running_jobs,queue_jobs
     running_jobs[i] = subprocess.Popen(queue_jobs.pop(), stderr=errorFILE, shell = True)
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
         running_jobs.append(subprocess.Popen(queue_jobs.pop(), stderr=errorFILE, shell = True))

config = ''
def importSettings(settingsFileName):
    global config
    config = imp.load_source('config', '.config.py')

def reloadLib():
    global config
    config = imp.load_source('config', '.config.py')

    # TODO
    # reload doesnt work, dont know why
    #reload(config)
