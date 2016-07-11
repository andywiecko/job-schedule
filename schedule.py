#!/bin/python
import os
import subprocess



process = subprocess.Popen('sleep 10;ls -lotr &', shell = True)
for i in range(11):
    os.system('sleep 1')
    print process.pid,process.poll()

