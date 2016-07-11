#!/bin/python
import os
import subprocess
import time

max_running_jobs = 4
sync_time = 3



# list with running jobs
running_jobs     = []
# stack with jobs in queue
queue_jobs       = []

#load file with jobs
queue_jobs = open('jobs.txt','r').read().split('\n')[:-1]

all_jobs = len(queue_jobs)
done_jobs = 0

#init first jobs
for i in range(max_running_jobs):
    running_jobs.append(subprocess.Popen(queue_jobs.pop(), shell = True))


while (queue_jobs != []):
    time.sleep(sync_time)
    for i in range(max_running_jobs):
        proc = running_jobs[i]
        
        if proc.poll() == 0:
            if queue_jobs == []: break
            running_jobs[i] = subprocess.Popen(queue_jobs.pop(), shell = True)
            done_jobs += 1
            print 'jobs done: ',done_jobs,'/', all_jobs,' (workers: ',len(running_jobs),')'

while (running_jobs != []):
    time.sleep(sync_time)
    for proc in running_jobs:

        if proc.poll() == 0:
            running_jobs.remove(proc)
            done_jobs += 1
            print 'jobs done: ',done_jobs,'/', all_jobs,' (workers: ',len(running_jobs),')'

