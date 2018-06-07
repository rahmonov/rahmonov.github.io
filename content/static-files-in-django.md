Title: Django Static Files
Date: 2018-06-07 20:10
Modified: 2018-06-07 20:10
Category: python
Tags: programming, python
Slug: django-static-files
Authors: Jahongir Rahmonov
Summary: Django Static Files for Dummies

Have you ever been frustrated when your Django application did not find the static files you were using?
Then, you read the documentation and played around with all those settings variables and after a couple of hours it was finally fixed.
However, you had no idea what you just did. I have been in this situation so many times that I decided to write
this post where I explain everything you need to configure your static files in a Django application.

The **first** thing you need to know is that static files are stored at `$APP/static/` where `$APP` is an application name:

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/django-static-files/django-static-files.jpg" rel="lightbox" title="first">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/django-static-files/django-static-files.jpg" alt="first">
    </a>
</div>

These are usually static files such as css and javascript files that are related to that `$APP`.

You can **also** tell Django to look for static files in some arbitrary locations of your choice. You use `STATICFILES_DIRS` for that:

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "unrelatedstatic")
]
```

These are usually static files that are not related to any app that you have in your Django application.

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/django-static-files/static-files-dirs.jpg" rel="lightbox" title="Staticfiles dirs">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/django-static-files/static-files-dirs.jpg" alt="Staticfiles dirs">
    </a>
</div>

Now, keep in mind that these different folders are where you store your static assets **DURING DEVELOPMENT**. When you deploy your app to the production,
you want to configure your web server (e.g. [NGINX](/posts/run-a-django-app-with-nginx-gunicorn-and-supervisor/)) to look for static files in one
single location rather than multiple paths. How do you collect all your static files from different apps to a single folder? As simple as this:

```python
python manage.py collectstatic
```

However, this will throw an exception because it does not know where to collect the files yet. You need to tell it by setting the `STATIC_ROOT` setting:

```python
STATIC_ROOT = os.path.join(BASE_DIR, "allstaticfiles")
```

Now run that command and all you static files will be collected to `allstaticfiles` folder in your project root:

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/django-static-files/collectstatic.png" rel="lightbox" title="Collectstatic">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/django-static-files/collectstatic.png" alt="Collectstatic">
    </a>
</div>

Again, you **DON'T PUT** any static file in `STATIC_ROOT`. That's where files get collected automatically after you run `collectstatic`.

Now, in production, you can configure your web server to serve static files from that location. In NGINX, it would look like this:

```bash
location /static/ {
    root   /my/project/allstaticfiles/;
}
```

And the last piece is to set `STATIC_URL` to your `STATIC_ROOT` so that when you do `{% static 'main.css' %}` in a django template, it uses the `allstaticfiles` folder in production.

Again, `STATIC_URL` is set to `static` during development and to `STATIC_ROOT` in production:

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/django-static-files/production.png" rel="lightbox" title="result">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/django-static-files/production.png" alt="result">
    </a>
</div>

I learned this while attending [DjangoCon Europe 2018](https://2018.djangocon.eu/) and thus all credits go to [Curtis Maloney](https://github.com/funkybob) who
presented this in a lighting talk. It made my life easier and I hope it does the same for everybody else.

Fight on!
