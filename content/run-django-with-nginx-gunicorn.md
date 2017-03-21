Title: Run a Django app with Nginx and Gunicorn in Ubuntu 16.04 (Part II)
Date: 2017-02-26 20:10
Modified: 2017-02-26 20:10
Category: programming
Tags: python, django, gunicorn, nginx
Slug: run-a-django-app-with-nginx-and-gunicorn
Authors: Jahongir Rahmonov
Summary: How to run a Django app with Nginx and Gunicorn

This tutorial is the continuation of [this one](http://rahmonov.me/posts/run-a-django-app-with-gunicorn-in-ubuntu-16-04/) where we learned
how to run a django app with gunicorn. Now we will add Nginx into the mix.

The reason we need Nginx
------------------------
If you followed the previous tutorial, we ran our django app with Gunicorn. However, at the end, we saw that the styles of the admin
panel were gone. The reason is that Gunicorn is an application server and just runs the app (django app in our case) and django, as we know,
does not serve static files except in development. Nginx to the rescue! It will be a reverse proxy for Gunicorn. What the hell is a reverse proxy?
Good question! We all know what VPNs are, right? We use them to access some website that is blocked for some reason. In this case, we access
that website through a VPN: We -> VPN -> some website. This kind of proxies are called Forward Proxies. As for reverse proxies, think of
them as forced proxies. For example, a user is trying to access our django app running in gunicorn. He thinks that he is accessing the app directly.
However, what is happening is that he is first accessing the Nginx server which decides what to do next. If the user is accessing a static file,
the Nginx server will serve it itself. Otherwise, it will redirect it to Gunicorn. In plain terms, http requests will be handled by
Gunicorn and static ones by Nginx. That's why we need Nginx.
 
Apart from that, Nginx also improves performance, reliability, security and scale.


Installation
------------
By now we already have Django and Gunicorn ready. So, let's install Nginx now:

    :::bash
    sudo apt-get install nginx

Now, we will configure Nginx to pass traffic to the process.

Create a file `/etc/nginx/sites-available/djtrump` and type in the following:
    
    :::bash
    server {
        listen 8000;
        server_name 0.0.0.0;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static/ {
                root /home/ubuntu/myproject;
        }

        location / {
                include proxy_params;
                proxy_pass http://unix:/home/ubuntu/myproject/myproject.sock;
        }
    }

Adjust the paths such as `/home/ubuntu/myproject` to your own environment.

Let's see what is going on here.

The first two lines tell that it will listen to the port `8000` on `0.0.0.0`. The next line about favicon will tell Nginx to ignore
problems with favicon.ico.

The next block is very important. It says that static files, which all have a standard URI prefix of `static/` should be looked for in
`~/myproject/static/` folder.
 
And the last location block matches all other requests other that static ones (remember reverse proxy). One thing to note here is that Nginx and Gunicorn "talk to" 
each other through a unix socket. That's why we will bind our gunicorn to a socket as we will see soon.
  
Now, let's enable this file by linking it to the `sites-enabled` folder:
  
    :::bash
    sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
      
and check if our configuration file was correctly written:

    :::bash
    sudo nginx -t
    
If everything is OK, you should see something like this:

    :::bash
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful

You may ask what all that linking and `sites-enabled` folder were about. We could have included those settings in Nginx's main settings file:
`/etc/nginx/nginx.conf`. If we take a look at it, we will see this:

    :::bash
    include /etc/nginx/sites-enabled/*
    
So, we can see that what we did makes it more modular and much easier to maintain when we have several apps being served by Nginx.

OK, now that we have configured Nginx, let's see some action.

First, let's move all our static files to `~/myproject/static/` because we set up Nginx to look for them there.
Open up `myproject/settings.py` and add this:
 
 
    :::python
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
     
     
Save and close. Now, let's collect them to that folder:

    :::bash
    ./manage.py collectstatic
    
Confirm the operation and our static files should be there for Nginx to find them.

Now, let's finally run our app:
 
    :::bash
    gunicorn --daemon --workers 3 --bind unix:/home/ubuntu/myproject/myproject.sock myproject.wsgi

As I told earlier, we are starting gunicorn a little differently now. We are binding it to a unix socket file which is needed to talk
to Nginx. This file will be created and enable Nginx and Gunicorn to talk to each other. You may ask what about ports and ip?.
Nginx will take care of that. Remember we configured it to listen to `0.0.0.0:8000`? Cool! Now, let's restart Nginx to make these changes
take effect.

    :::bash
    sudo service nginx restart

Now, go ahead and access `0.0.0.0:8000`. Great, our app is running. Let's check our admin panel now at `0.0.0.0:8000/admin`. Awesome,
styles are there! We have achieved what we wanted. Congratulations!

This is just the tip of the iceberg. You will need more stuff as your app grows. Go to [nginx docs](https://nginx.org/en/docs/) to learn more.

In the next tutorial, we will take a look at `supervisord` to make process management very easy.

Fight on!

[Part I](http://rahmonov.me/posts/run-a-django-app-with-gunicorn-in-ubuntu-16-04/)

[Part III](http://rahmonov.me/posts/run-a-django-app-with-nginx-gunicorn-and-supervisor/)
 