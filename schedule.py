#!/bin/python
import os
import subprocess

max_running_jobs = 4
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
    os.system('sleep 1')
    for i in range(max_running_jobs):
        proc = running_jobs[i]
        print proc.pid,proc.poll()

        if proc.poll() == 0:
            running_jobs[i] = subprocess.Popen(queue_jobs.pop(), shell = True)
            done_jobs += 1
            print 'jobs done: ',done_jobs,'/', all_jobs

    print ''

while (running_jobs != []):
    os.system('sleep 1')
    for proc in running_jobs:
        print proc.pid,proc.poll()

        if proc.poll() == 0:
            running_jobs.remove(proc)
            done_jobs += 1
            print 'jobs done: ',done_jobs,'/', all_jobs

    print ''





#for i in job_file:
#    print i
#    running_jobs.append(subprocess.Popen(i, shell = True))
#
#for i in range(11):
#    os.system('sleep 1')
#    for i in running_jobs:
#        print i.pid,i.poll()
#    
#    
#print process.pid,process.poll()

