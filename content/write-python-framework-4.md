Title: How to write a Python web framework. Part IV.
Date: 2019-03-25 20:10
Modified: 2019-03-25 20:10
Category: python
Tags: programming, python
Slug: write-python-framework-part-four
Authors: Jahongir Rahmonov
Summary: The fourth post of the series where we will be writing our own Python framework just like Flask and Django.

*Check out Part I [here](/posts/write-python-framework-part-one/)*<br>
*Check out Part II [here](/posts/write-python-framework-part-two/)*<br>
*Check out Part III [here](/posts/write-python-framework-part-three/)*

> A little reminder that this series is based on the [Alcazar framework](https://github.com/rahmonov/alcazar) that I am writing for
learning purposes. If you liked this series, show some love by starring the [repo](https://github.com/rahmonov/alcazar).

In the previous blog posts in the series, we started writing our own Python framework and implemented
the following features:

- WSGI compatibility
- Request Handlers
- Routing: simple and parameterized
- Check for duplicate routes
- Class Based Handlers
- Unit tests
- Test Client
- Alternative way to add routes (like Django)
- Support for templates

In this part, we will add a few more awesome features to the list:

- Custom exception handler
- Support for static files
- Middleware

## Custom exception handler

Exceptions inevitably happen. Users may do something that we didn't expect. We may write some code that doesn't work
on some occasions. Users may go to a non existent page. With what we have right now, if some exception happens, we show a big
ugly `Internal Server Error` message. Instead, we could show some nice one. Something along the lines of `Oops! Something went wrong.` or
`Please, contact our customer support`. For that, we need to be able to catch those exceptions and handle them however we want.

It will look like this:

```python
# app.py
from api import API

app = API()

def custom_exception_handler(request, response, exception_cls):
    response.text = "Oops! Something went wrong. Please, contact our customer support at +1-202-555-0127."

app.add_exception_handler(custom_exception_handler)
```

Here we create a custom exception handler. It looks almost like our simple request handlers, except that it has `exception_cls` as its
third argument. Now, if we have a request handler that throws an exception, this above-mentioned custom exception handler should be called.

```python
# app.py

@app.route("/home")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be user")
```

If we go to `http://localhost:8000/home`, instead of our previous big ugly `Internal Server Error`, we should be able to see our custom message of
`Oops! Something went wrong. Please, contact our customer support at +1-202-555-0127.`. Does it look good enough? Let's go ahead and implement it.

The first thing we need is a variable inside our main API class where we will store our exception handler:

```python
# api.py

class API:
    def __init__(self, templates_dir="templates"):
        ...
        self.exception_handler = None
```

Now we need to add the `add_exception_handler` method:

```python
# api.py

class API:
    ...

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler
```

Having registered our custom exception handler, we need to call when an exception happens. Where do exceptions happen? That's right:
when handlers are called. We call the handlers inside our `handle_request` method. So, we need to wrap it with a try/except clause and
call our custom exception handler in the `except` part:

```python
# api.py

class API:
    ...

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError("Method now allowed", request.method)

                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)

        return response
```

We also need to make sure that if no exception handler has been registered, the exception is propagated.

We have everything in place. Go ahead and restart your gunicorn and go to `http://localhost:8000/home`. You should see our little cute message instead of the big ugly default one.
Of course, make sure that you have the above mentioned exception handler and the errorful request handler in the `app.py`.

If you want to go one step further, create a nice template and use our `api.template()` method inside the exception handler.
However, our framework doesn't support static files and thus you will have hard time designing your template with CSS and JavaScript.
Don't get sad because this is exactly what we are doing next.

## Support for static files

Templates are not truly templates without good CSS and JavaScript, are they? Shall we add a support for such files then?

Just like we used Jinja2 for template support, we will use [WhiteNoise](http://whitenoise.evans.io/en/stable/) for static file serving.
Install it:

```shell
pip install whitenoise
```

WhiteNoise is pretty simple. The only thing that we need to do is wrap our WSGI app and give it the static folder path as a parameter.
Before we do that, let's remember how our `__call__` method looks like:

```python
# api.py

class API:
    ...

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    ...
```

This is basically an entrypoint to our WSGI app and this is exactly what we need to wrap with WhiteNoise. Thus, let's refactor its content to a
separate method so that it will be easier to wrap it with WhiteNoise:

```python
# api.py

class API:
    ...

    def wsgi_app(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
```

Now, in our constructor, we can initialize a WhiteNoise instance:

```python
# api.py
...
from whitenoise import WhiteNoise


class API:
    ...
    def __init__(self, templates_dir="templates", static_dir="static"):
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(templates_dir))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
```

As you can see, we wrapped our `wsgi_app` with WhiteNoise and gave it a path to the static folder as the second param.
The only thing left to do is make this `self.whitenoise` an entrypoint to our framework:

```python
# api.py

class API:
    ...
    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)
```

With everything in place, create `static` folder in the project root, create the `main.css` file inside and put the following into it:

```css
body {
    background-color: chocolate;
}
```

In the [third blog post](/posts/write-python-framework-part-three/), we created the `templates/index.html`. Now we can put our newly created css file inside this template:

```html
<html>
    <header>
        <title>{{ title }}</title>

        <link href="/main.css" type="text/css" rel="stylesheet">
    </header>

    <body>
        <h1>The name of the framework is {{ name }}</h1>
    </body>

</html>
```

Restart your gunicorn and go to `http://localhost/template`. You should see that the color of the whole background is chocolate, not white, meaning
that our static file is being served. Awesome!

## Middleware

If you need a little recap of what middlewares are and how they work, go read [this post](/posts/what-the-hell-is-wsgi-anyway-and-what-do-you-eat-it-with/) first. Otherwise, this part
may seem a little confusing. I will wait. Back? Great. Let's go.

You know what they are and how they work but you may be wondering what they are used for. Basically, middleware is a component that can modify
an HTTP request and/or response and is designed to be chained together to form a pipeline of behavioral changes during request processing.
Examples of middleware tasks can be request logging and HTTP authentication. The main point is that none of these is fully responsible
for responding to a client. Instead, each middleware changes the behavior in some way as part of the pipeline, leaving the actual
response to come from something later in the pipeline. In our case, that something that actually responds to a client is our request handlers.
Middlewares are wrappers around our WSGI app that have the ability to modify requests and responses.

From the bird's eye view, the code will look like this:

```python
FirstMiddleware(SecondMiddleware(our_wsgi_app))
```

So, when a request comes in, it first goes to `FirstMiddleware`. It modifies the request and sends it over to `SecondMiddleware`.
Now, `SecondMiddleware` modifies the request and sends it over to `our_wsgi_app`. Our app handles the request, prepares the response and sends it back to
`SecondMiddleware`. It can modify the response if it wants and send it back to `FirstMiddleware`. It modifies the response and sends it back
to the web server (e.g. gunicorn).

Let's go ahead and create a `Middleware` class that other middlewares will inherit from and that wraps our wsgi app.

Create a `middleware.py` file first:

```shell
touch middleware.py
```

Now, we can begin our `Middleware class`:

```python
# middleware.py

class Middleware:
    def __init__(self, app):
        self.app = app
```

As we mentioned above, it should wrap a wsgi app and in case of multiple middlewares that `app` can also be another middleware.

As a base middleware class, it should also have the ability to add another middleware to the stack:

```python
# middleware.py

class Middleware:
    ...

    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)
```

It is simply wrapping the given middleware class around our current app.

It should also have its main methods which are request processing and response processing. For now, they will do nothing.
The child classes that will inherit from this class will implement these methods:

```python
# middleware.py

class Middleware:
    ...

    def process_request(self, req):
        pass

    def process_response(self, req, resp):
        pass
```

Now, the most important part, the method that handles incoming requests:

```python
# middleware.py

class Middleware:
    ...

    def handle_request(self, request):
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response
```

It first calls the `self.process_request` to do something with the request. Then delegates the response creation to the app that it is wrapping.
Finally, it calls the `process_response` to do something with the response object. Then simply returns the response upward.

As middlewares are the first entrypoint to our app now, they are the ones called by our web server (e.g. gunicorn). Thus, middlewares should implement the
WSGI entrypoint interface:

```python
# middleware.py
from webob import Request

class Middleware:

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)
```

It is just a copy of the `wsgi_app` function we created above.

With our Middleware class implemented, let's add it to our main `API` class:

```python
# api.py
...
from middleware import Middleware


class API:
    def __init__(self, templates_dir="templates", static_dir="static"):
        ...
        self.middleware = Middleware(self)
```

It wraps around `self` which is our wsgi app. Now, let's give it the ability to add middlewares:

```python
# api.py

class API:
    ...

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
```

The only thing left to do is call this middleware in the entrypoint instead of our own wsgi app:

```python
# api.py

class API:
    ...

    def __call__(self, environ, start_response):
        return self.middleware(environ, start_response)
```

Why do you ask? Because we are delegating the job of being an entrypoint to the middlewares now. Remember that we implemented WSGI entrypoint
interface inside our `Middleware` class. Let's go ahead now and create a simple middleware that simply prints to the console:

```python
# app.py
from api import API
from middleware import Middleware

app = API()

...

class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, res):
        print("Processing response", req.url)

app.add_middleware(SimpleCustomMiddleware)

...
```

Restart your gunicorn and go to any url (e.g. `http://localhost:8000/home`). Everything should work just like before. The only exception is that those texts should appear in
the console. Open your console and you should see the following:

```shell
Processing request http://localhost:8000/home
Processing response http://localhost:8000/home
```

There is a catch. Have you found it? Static files don't work now. The reason is that we stopped using `WhiteNoise`.
We removed it. Instead of calling `WhiteNoise`, we are calling the middleware. Here is what we should do. We need to distinguish between
requests for static files and the others. When a request is coming in for a static file, we should call `WhiteNoise`. For others,
we should call the middleware. The question is how do we distinguish between them. Right now, requests for static files look like this:
`http://localhost:8000/main.css`. Other requests look like this `http://localhost:8000/home`. They look the same for our `API` class.
Thus we will add a root to the URLs of static files so that they look like this `http://localhost:8000/static/main.css`.
We will check if the request path starts with `/static`. If so, we will call `WhiteNoise`, otherwise we will call the middleware.
We should also make sure to cut the `/static` part. Otherwise `WhiteNoise` won't find the files:

```python
# api.py

class API:
    ...

    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]

        if path_info.startswith("/static"):
            environ["PATH_INFO"] = path_info[len("/static"):]
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)
```

Now, in the templates, we should call static files like so:

```html
<link href="/static/main.css" type="text/css" rel="stylesheet">
```

Go ahead and change your `index.html`.

Restart your gunicorn and check that everything is working properly.

We will use this middleware feature in the future posts to add authentication to our apps.

I think that this middleware part is more difficult to understand compared to others. I also think that I didn't do a great job
explaining it. Thus, please write the code, let it sink in and ask me questions in the comments if something is not clear.

*Check out Part I [here](/posts/write-python-framework-part-one/)*<br>
*Check out Part II [here](/posts/write-python-framework-part-two/)*<br>
*Check out Part III [here](/posts/write-python-framework-part-three/)*

> A little reminder that this series is based on the [Alcazar framework](https://github.com/rahmonov/alcazar) that I am writing for
learning purposes. If you liked this series, show some love by starring the [repo](https://github.com/rahmonov/alcazar).

That's it from me today.

Fight on!
