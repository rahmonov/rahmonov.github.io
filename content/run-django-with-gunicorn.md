Title: Run a Django app with Gunicorn in Ubuntu 16.04 (Part I)
Date: 2017-02-21 20:10
Modified: 2017-02-21 20:10
Category: programming
Tags: python, django, gunicorn
Slug: run-a-django-app-with-gunicorn-in-ubuntu-16-04
Authors: Jahongir Rahmonov
Summary: How to run a Django app with Gunicorn instead of a development server

This tutorial is aimed at beginners and is a part of a series where we learn to run a django app with Gunicorn and Nginx, and manage
it with the help of the Supervisord. Basically, we are trying to emulate a production environment.

The Problem
-----------
We are all very well aware that we can run our django app simply by executing a `./manage.py runserver` command. We also know that it is
called a *development* server for a reason. You know it is not robust, security issues, thread issues and etc. So, how do we *really* run
our app then?
 
The Solution 
------------
Enter [Gunicorn](http://gunicorn.org/), a simple, light and speedy Python WSGI HTTP Server for UNIX. We will see how to use gunicorn now 
but it is not the main reason I wrote this tutorial. The main reason is this: back in the day I was terrified at the thought of anything
related to *production vs development* stuff because I thought, you know, **THESE ARE NGINX and GUNICORN** which can support millions of
requests per second and are very secure/robust/reliable and thus should be very difficult to learn and configure. I want to prevent others
from experiencing the same and demonstrate that it is really **simple** and **simple**.
   
Enough talk, let's fight! (YAY, always wanted to quote Kung Fu Panda)
    
Installation
------------

First, let's go ahead and update/upgrade our packages:
    
```bash
sudo apt-get update
sudo apt-get upgrade
```
    
Now, install `pip`.
If you are using python2, type the following:

```bash
sudo apt-get install python-pip
``` 

If you are instead using python3, type the following:

```bash
sudo apt-get install python3-pip
```    
    
Now install `virtualenv`:
For python2:
 
```bash
sudo pip install virtualenv
``` 

For python3:

```bash
sudo pip3 install virtualenv
```

Let's go ahead now and install a virtual environment at `/opt/envs/myprojenv`. You can install it anywhere you like and in real life use 
a more descriptive name for the virtualenv:
 
```bash
virtualenv /opt/envs/myprojenv
```
    
Activate it:

```bash
source /opt/envs/myprojenv/bin/activate
```
    
You should now see `(myprojenv)` at the beginning of your command line.

Now, install Django. By the way, we will only use `pip` from now on, not `pip3`, as we are inside a virtual environment:

```bash
pip install django
```
    
Create a project:

```bash
django-admin startproject myproject
```
    
Apply migrations and run the development server:

```bash
cd myproject
./manage.py migrate
./manage.py runserver
```
     
Go to `localhost:8000/admin` and make sure that it is running. Is it running? Cool! Easy right?!
Now we will replace this development server with gunicorn and you will see that it is **as easy**.

Install gunicorn:

```bash
pip install gunicorn
```
 
Run this, go to `localhost:8000`and behold the magic:

```bash
gunicorn myproject.wsgi
```
  
DO YOU SEE IT? It is this easy.

Now you might be wondering what is that `wsgi` thing is. Well, it stands for Web Server Gateway Interface and basically is a way how
apps/frameworks and servers talk to each other. If the server(like Gunicorn) has `wsgi` implemented and so has your framework(Django),
it means that you can run your app with that server. And the entry point of communication for these two is the variable `application`,
which is located in `myproject/wsgi.py` in our case. You can read more about this in [PEP 333](https://www.python.org/dev/peps/pep-0333/). 
 
Let's play with it a little bit to see what it got.

We can bind it to a specific port:

```bash
gunicorn --bind 0.0.0.0:8030 myproject.wsgi
```
   
You can increase the number of workers to serve requests, which you probable will in real life as your users increase:
   
```bash
gunicorn --workers 3 myproject.wsgi
```    
    
Run it in a daemon mode:

```bash
gunicorn --daemon myproject.wsgi
```
    
Or all of them altogether(a shorter version):

```bash
gunicorn -d -b 0.0.0.0:8030 -w 3 myproject.wsgi
```
    
Read more about these options [in the docs](http://docs.gunicorn.org/en/stable/run.html#commonly-used-arguments)

If these options get too long, you can create an `ini` file and run it like this:

```bash
gunicorn -c /path/to/config/file myproject.wsgi
```
   
After running your app with gunicorn, go to the django admin panel at `localhost:8000/admin`. You will see that all styles are gone.
The reason is that gunicorn is an application server and it does not serve static files. In order to solve this problem, we will take a look
at `Nginx` next and use it as a reverse proxy for gunicorn. We will talk about what `reverse proxy` is as well so don't think about it for now.

Well, that's it for now. This is a brief overview of django with gunicorn. Go to [docs](http://docs.gunicorn.org/en/stable/) and read more.

Fight on!

[Part II](/posts/run-a-django-app-with-nginx-and-gunicorn/)

[Part III](/posts/run-a-django-app-with-nginx-gunicorn-and-supervisor/)