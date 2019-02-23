Title: How to write a Python web framework. Part I.
Date: 2019-02-09 20:10
Modified: 2019-02-09 20:10
Category: python
Tags: programming, python
Slug: write-python-framework-part-one
Authors: Jahongir Rahmonov
Summary: This is the first of the series where we will be writing our own Python framework just like Flask and Django.

*Check out Part II [here](/posts/write-python-framework-part-two/)*

"Don't reinvent the wheel" is one of the most frequent mantras we hear every day. But what if I want to learn more about the wheel?
What if I want to learn how to make this damn wheel? I think it is a great idea to reinvent it for the purpose of learning. Thus, in these series,
we will write our own Python web framework to see how all that magic is done in Flask, Django and other frameworks.

In this first part of the series, we will build the most important parts of the framework. At the end of it, we will have request handlers (think Django views) and
routing: both simple (like `/books/`) and parameterized (like `/greet/{name}`). If you like it after reading, please let me know in the comments what other features we
should implement next.

Before I start doing something new, I like to think about the end result. In this case, at the end of the day, we want to be able to use this framework
in production and thus we want our framework to be served by a fast, lightweight, production-level application server. I have been using [gunicorn](https://gunicorn.org)
in all of my projects in the last few years and I am very satisfied with the results. So, let's go with `gunicorn`.

`Gunicorn` is a [WSGI](/posts/what-the-hell-is-wsgi-anyway-and-what-do-you-eat-it-with/) HTTP Server, so it expects a specific entrypoint to our application. If you don't know
what `WSGI` is [go find out](/posts/what-the-hell-is-wsgi-anyway-and-what-do-you-eat-it-with/), I will wait. Otherwise, you will not understand a huge chunk of this blog post.

Have you learnt what WSGI is? Good. Let's continue.

To be WSGI-compatible, we need a callable object (a function or a class) that expects two parameters (`environ` and `start_response`) and returns a WSGI-compatible response.
Don't worry if it doesn't make sense yet. Hopefully it will "click" for you while writing the actual code. So, let's get started with the code.

Think of a name for your framework and create a folder with that name. I named it `bumbo`:

```shell
mkdir bumbo
```

Go into this folder, create a virtual env and activate it:

```shell
cd bumbo
python3.6 -m venv venv
source venv/bin/activate
```

Now, create the file named `app.py` where we will store our entrypoint for `gunicorn`:

```shell
touch app.py
```

Inside this `app.py`, let's write a simple function to see if it works with `gunicorn`:

```python
# app.py

def app(environ, start_response):
    response_body = b"Hello, World!"
    status = "200 OK"
    start_response(status, headers=[])
    return iter([response_body])
```

As mentioned above, this entrypoint callable receives two params. One of them is `environ` where all kinds of info about request is stored such as a request method, url, query params and the like.
The second is `start_response` which starts the response as the name suggests. Now, let's try to run this code with `gunicorn`. For that install `gunicorn` and run it like so:

```shell
pip install gunicorn
gunicorn app:app
```

The first `app` is the file which we created and the second app is the name of the function we just wrote. If all is good, you will see something like the following in the output:

```shell
[2019-02-09 17:58:56 +0500] [30962] [INFO] Starting gunicorn 19.9.0
[2019-02-09 17:58:56 +0500] [30962] [INFO] Listening at: http://127.0.0.1:8000 (30962)
[2019-02-09 17:58:56 +0500] [30962] [INFO] Using worker: sync
[2019-02-09 17:58:56 +0500] [30966] [INFO] Booting worker with pid: 30966
```

If you see this, open your browser and go to `http://localhost:8000`. You should see our good old friend: the `Hello, World!` message. Awesome! We will build off of this.

Now, let's turn this function into a class because we will need quite a few helper methods and they are much easier to write inside a class. Create an `api.py` file:

```shell
touch api.py
```

Inside this file, create the following `API` class. I will explain what it does in a bit:

```python
# api.py

class API:
    def __call__(self, environ, start_response):
        response_body = b"Hello, World!"
        status = "200 OK"
        start_response(status, headers=[])
        return iter([response_body])
```

Now, delete everything inside `app.py` and write the following:

```python
# app.py
from api import API

app = API()
```

Restart your `gunicorn` and check the result in the browser. It should be the same as before because we simply converted our function named `app` to a class called `API` and overrode
its `__call__` method which is called when you call the instances of this class:

```python
app = API()
app()   #  this is where __call__ is called
```

Now that we created our class, I want to make the code more elegant because all those bytes (`b"Hello World"`) and `start_response` seem confusing to me.
Thankfully, there is a cool package called [WebOb](https://docs.pylonsproject.org/projects/webob/en/stable/index.html) that provides objects for HTTP requests and responses by
wrapping the `WSGI` request environment and response status, headers and body. By using this package, we can pass the `environ` and `start_response` to the classes provided by this package
and not have to deal with them ourselves. Before we continue, I suggest you take a look at the [documentation of WebOb](https://docs.pylonsproject.org/projects/webob/en/stable/index.html) to
understand what I am talking about and the API of `WebOb` more.

Here is how we will go about refactoring this code. First, install `WebOb`:

```shell
pip install webob
```

Import the `Request` and `Response` classes at the beginning of the `api.py` file:

```python
# api.py
from webob import Request, Response

...
```

and now we can use them inside the `__call__` method:

```python
# api.py
from webob import Request, Response

class API:
    def __call__(self, environ, start_response):
        request = Request(environ)

        response = Response()
        response.text = "Hello, World!"

        return response(environ, start_response)
```

Looks much better! Restart the `gunicorn` and you should see the same result as before. And the best part is I don't have to explain what is being done here. It is all self-explanatory.
We are creating a request, a response and then returning that response. Awesome! I do have to note that `request` is not being used here yet because we are not doing anything with it.
So, let's use this chance and use the request object as well. Also, let's refactor the `response` creation into its own method. We will see why it is better later:

```python
# api.py
from webob import Request, Response

class API:
    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        user_agent = request.environ.get("HTTP_USER_AGENT", "No User Agent Found")

        response = Response()
        response.text = f"Hello, my friend with this user agent: {user_agent}"

        return response
```

Restart your `gunicorn` and you should see this new message in the browser. Did you see it? Cool. Let's go on.

At this point, we handle all the requests in the same way. Whatever request we receive, we simply return the same response which is created in the `handle_request` method.
Ultimately, we want it to be dynamic. That is, we want to serve the request coming from `/home/` differently than the one coming from `/about/`.

To that end, inside `app.py`, let's create two methods that will handle those two requests:

```python
# app.py
from api.py import API

app = API()


def home(request, response):
    response.text = "Hello from the HOME page"


def about(request, response):
    response.text = "Hello from the ABOUT page"
```

Now, we need to somehow associate these two methods with the above mentioned paths: `/home/` and `/about/`. I like the Flask way of doing it that would look like this:

```python
# app.py
from api.py import API

app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"
```

What do you think? Looks good? Then let's implement this bad boy!

As you can see, the `route` method is a decorator, accepts a path and wraps the methods. It shouldn't be too difficult to implement:

```python
# api.py

class API:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    ...
```

Here is what we did here. In the `__init__` method, we simply defined a `dict` called `self.routes` where we will be storing paths as keys and handlers as values. It can look like this:

```python
print(self.routes)

{
    "/home": <function home at 0x1100a70c8>,
    "/about": <function about at 0x1101a80c3>
}
```

In the `route` method, we took path as an argument and in the wrapper method simply put this path in the `self.routes` dictionary as a key and the handler as a value.

At this point, we have all the pieces of the puzzle. We have the handlers and the paths associated with them. Now, when a request comes in, we need to check its `path`, find an appropriate handler,
call that handler and return an appropriate response. Let's do that:

```python
# api.py
from webob import Request, Response

class API:
    ...

    def handle_request(self, request):
        response = Response()

        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response

    ...
```

Wasn't too difficult, was it? We simply iterated over `self.routes`, compared paths with the path of the request, if there is a match, called the handler associated with that path.

Restart the `gunicorn` and try those paths in the browser. First, go to `http://localhost:8000/home/` and then go to `http://localhost:8000/about/`. You should see the corresponding messages. Pretty cool, right?

As the next step, we can answer the question of "What happens if the path is not found?". Let's create a method that returns a simple HTTP response of "Not found." with the status code of 404:

```python
# api.py
from webob import Request, Response

class API:
    ...

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    ...
```

Now, let's use it in our `handle_request` method:

```python
# api.py
from webob import Request, Response

class API:
    ...

    def handle_request(self, request):
        response = Response()

        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response

        self.default_response(response)
        return response

    ...
```

Restart the `gunicorn` and try some nonexistent routes. You should see this lovely "Not found." page. Now, let's refactor out finding a handler to its own method for the sake of readability:

```python
# api.py
from webob import Request, Response

class API:
    ...

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if path == request_path:
                return handler

    ...
```

Just like before, it is simply iterating over `self.route`, comparing paths with the request path and returning the handler if paths are the same. It returns `None` if no handler was found.
Now, we can use it in our `handle_request` method:

```python
# api.py
from webob import Request, Response

class API:
    ...

    def handle_request(self, request):
        response = Response()

        handler = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)

        return response

    ...
```

I think it looks much better and is pretty self explanatory. Restart your `gunicorn` to see that everything is working just like before.

At this point, we have routes and handlers. It is pretty awesome but our routes are simple. They don't support keyword parameters in the url path.
What if we want to have this route of `@app.route("/hello/{person_name}")` and be able to use this `person_name` inside our handlers like this:

```python
def say_hello(request, response, person_name):
    resp.text = f"Hello, {person_name}"
```

For that, if someone goes to the `/hello/Matthew/`, we need to be able to match this path with the registered `/hello/{person_name}/` and find the appropriate handler.
Thankfully, there is already a package called `parse` that does exactly that for us. Let's go ahead and install it:

```bash
pip install parse
```

Let's test it out:

```bash
>>> from parse import parse
>>> result = parse("Hello, {name}", "Hello, Matthew")
>>> print(result.named)
{'name': 'Matthew'}
```

As you can see, it parsed the string `Hello, Matthew` and was able to identify that `Matthew` corresponds to the `{name}` that we provided.

Let's use it in our `find_handler` method to find not only the method that corresponds to the path but also the keyword params that were provided:

```python
# api.py
from webob import Request, Response
from parse import parse

class API:
    ...

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    ...
```

We are still iterating over `self.routes` and now instead of comparing the path to the request path, we are trying to parse it and if there is a result, we are returning both the handler and keyword params as a dictionary.
Now, we can use this inside `handle_request` to send those params to the handlers like this:

```python
# api.py
from webob import Request, Response
from parse import parse

class API:
    ...

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    ...
```

The only changes are, we are getting both `handler` and `kwargs` from `self.find_handler`, and passing that `kwargs` to the handler like this `**kwargs`.

Let's write a handler with this type of route and try it out:

```python
# app.py
...

@app.route("/hello/{name}")
def greeting(request, response, name):
    resp.text = f"Hello, {name}"

...
```

Restart your `gunicorn` and go to `http://localhost:8000/hello/Matthew/`. You should the wonderful message of `Hello, Matthew`. Awesome, right?
Add a couple more such handlers of yours. You can also indicate the type of the given params. For example you can do `@app.route("/tell/{age:d}")` so that you have the param
`age` inside the handler as a digit.


## Conclusion

This was a long ride but I think it was great. I personally learned a lot while writing this. If you liked this blog post, please let me know in the comments what other
features we should implement in our framework. I am thinking of class based handlers, support for templates and static files.

Fight on!

*Check out Part II [here](/posts/write-python-framework-part-two/)*
