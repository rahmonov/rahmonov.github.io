Title: Introduction to Celery
Date: 2016-04-28 20:10
Modified: 2016-04-28 20:10
Category: programming
Tags: celery, pyton, asynch, threads
Slug: indroduction-to-celery
Authors: Jahongir Rahmonov
Summary: Introduction to Celery: a simple, flexible and reliable distributed task queue

According to the [docs](http://docs.celeryproject.org/en/latest/index.html), Celery is a simple, 
flexible and reliable distributed system to process vast amounts of messages, while providing 
operations with the tools required to maintain such a system.

It’s a task queue with focus on real-time processing, while also supporting task scheduling.

What is it used for?
--------------------

It is mainly used for the following things:

 - Running something in the background
 - Asynchronous execution of code
 - Scheduling periodic work
 
Use case example
----------------

Your web app needs to send an email. That is a very slow operation. While users can put up with 4 or 5
seconds until an email is sent, it might leave a bad impression on them. Solution? Celery (singing...
"I came in like a wrecking ball...(by Miley Cyrus)")! It will take this operation out of the main thread and executes it
in the background. This gives the user the impression of good performance and “snappiness”, even 
though the real work might actually take some time.

Read [Queue everything and delight everyone](http://decafbad.com/blog/2008/07/04/queue-everything-and-delight-everyone/)
for additional info on why task queues can be useful.

Get started
-----------

Now that we know what Celery is and what it is used for, let's jump in and see how to use it with Django
(other cases should be similar). We will see how to send an email with Celery.

First, create a new `proj/proj/celery.py` module that defines a Celery instance

    :::python
    from __future__ import absolute_import

    import os
    
    from celery import Celery
    
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
    
    from django.conf import settings  # noqa
    
    app = Celery('proj')
    
    # Using a string here means the worker will not have to
    # pickle the object when using Windows.
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

Then, import this app in `proj/proj/__init__.py `

    :::python
    from __future__ import absolute_import

    # This will make sure the app is always imported when
    # Django starts so that shared_task will use this app.
    from .celery import app as celery_app  # noqa

Then, create an ordinary function

    :::python    
    def send_email():
        message = EmailMessage('Subject', 'Message', to=['jrahmonov2@gmail.com'])  
        message.send()
        print('Email is sent')
        
Note that tasks are normally placed in `tasks.py` file inside django apps:

    - app1/
        - app1/tasks.py
        - app1/models.py
    - app2/
        - app2/tasks.py
        - app2/models.py
        
However, for this simple example, I put the `send_email()` function inside `proj/proj/celery.py`

Now, let's check our function by executing it in the shell

    :::python
    >>> from celery_demo.celery import send_email 
    >>> send_email()

After a couple of seconds, you will see `Email is sent` message as long as you properly configured email settings.
But these seconds are too long when you can easily get rid of them. To do that, we now need to transform
this function into a celery task by simply using `@shared_task` decorator:

    :::python
    @shared_task()
    def send_email():
        message = EmailMessage('Subject', 'Message', to=['jrahmonov2@gmail.com'])
        message.send()
        print('Email is sent')

Now, we start celery in the command line by executing this:

    celery -A celery_demo worker -l info
    
Now, we call our task from the shell with `delay()` method of celery:

    >>> from celery_demo.celery import send_email
    >>> send_email.delay()
    
You will immediately see that the method returned! That means that users will see the results right away!
If you check you Celery logs, you will see something like this:

    [2016-04-28 06:54:59,920: INFO/MainProcess] Received task: celery_demo.celery.send_email[1d2b9446-4791-4da4-8136-ee74d78cf394]
    [2016-04-28 06:55:02,470: WARNING/Worker-3] Email is sent
    [2016-04-28 06:55:02,471: INFO/MainProcess] Task celery_demo.celery.send_email[1d2b9446-4791-4da4-8136-ee74d78cf394] succeeded in 2.550240921s: None

Awesome! Pretty fast!

This was a simple example of how to use Celery. Please note that this post does not discuss the installation process of Celery (or RabbitMQ) and is only
intended to serve as a fast introduction to the tool. 

In the next post, I will discuss how Celery can be used for periodic tasks (think cron jobs)

Fight on!



