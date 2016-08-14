Title: Periodic Tasks with Celery
Date: 2016-05-20 20:10
Modified: 2016-05-20 20:10
Category: programming
Tags: celery, python, asynch, threads, periodic
Slug: periodic-tasks-with-celery
Authors: Jahongir Rahmonov
Summary: How to implement periodic tasks with Celery

Celery is a task queue with focus on real-time processing, while also supporting task scheduling.
In the [previous post](http://rahmonov.me/posts/indroduction-to-celery/), we saw how celery can be 
used to take tasks out of main thread and process them in background. Now, we will take a look at its
task scheduling feature.

Use case example
----------------

As part of your company's marketing campaign, you want to periodically send emails to your customers 
informing them about new products and features. Besides, you want to send those emails at 9:30 a.m. every day
to make sure people see them when they just arrived in their office. You don't want to be doing it manually.
Celery to the rescue!

Get started
-----------

Now that we know we want to accomplish, we will see a simple example. Good news is that it is extremely easy to 
set up a periodic task.

First, let's write a function that simply says `Hello, name` in proj/tasks.py:

    :::python
    def say_hello(name):
        print("Hello, {}".format(name))
         
Now, in your settings file, write the following down:

    :::python
    CELERYBEAT_SCHEDULE = {
        'say-hello-every-30-seconds': {
            'task': 'tasks.say_hello',
            'schedule': timedelta(seconds=30),
            'args': ["Blog reader"]
        },
    }
    CELERY_TIMEZONE = 'UTC'    

I guess it is pretty clear what these settings mean. They simply say that `tasks.say_hello` should be 
executed every 30 seconds and given an argument `Blog reader`.

By the way, this feature of celery is called `celery-beat`.

Now, in command line, do the following:

    :::bash
    celery -A celery_demo beat

and behold! Every 30 seconds you will see something like this:

    :::python
    [2016-08-14 13:06:44,087: INFO/MainProcess] Scheduler: Sending due task say-hello-every-30-seconds (tasks.say_hello)
    [2016-08-14 13:07:14,114: INFO/MainProcess] Scheduler: Sending due task say-hello-every-30-seconds (tasks.say_hello)  

Pretty awesome, huh?
      
If you want more flexibility of when the task is executed, take a look at [crontab](http://docs.celeryproject.org/en/latest/reference/celery.schedules.html#celery.schedules.crontab)
With that, you can execute your tasks at any time you want. For example: Execute every ten minutes, but only between 3-4 am, 5-6 pm and 10-11 pm on Thursdays or Fridays.

Told you it is very easy :)

Fight on!
