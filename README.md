# job-schedule
schedule proceses on linux using python2.7

example:

To run jobs from a file with default number of workers:

~~~
python schedule.py jobs.txt       
~~~

To run jobs from a file with set sync time [ms]:

~~~
python schedule.py jobs.txt 0.5
~~~

To change number of workers just edit `.config.py` file.

Current status and occured errors one see in `.status` and `.errors` files respectively.


