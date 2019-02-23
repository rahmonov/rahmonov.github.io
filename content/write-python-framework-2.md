Title: How to write a Python web framework. Part II.
Date: 2019-02-23 20:10
Modified: 2019-02-23 20:10
Category: python
Tags: programming, python
Slug: write-python-framework-part-two
Authors: Jahongir Rahmonov
Summary: The second post of the series where we will be writing our own Python framework just like Flask and Django.

In the [first part](/posts/write-python-framework-part-one/), we started writing our own Python framework and implemented
the following features:

- WSGI compatible
- Request Handlers
- Routing: simple and parameterized

Make sure to read [Part I](/posts/write-python-framework-part-one/) of these series before this one.

This part will be no less exciting and we will add the following features in it:

- Check for duplicate routes
- Class Based Handlers
- Unit tests

Ready? Let's get started.

## Duplicate routes

Right now, our framework allows to add the same route any number of times. So, the following will work:

```python
@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/home")
def home2(request, response):
    response.text = "Hello from the SECOND HOME page"
```

The framework will not complain and because we use a Python dictionary to store routes, only the last one will work if you go to `http://localhost:8000/home/`.
Obviously, this is not good. We want to make sure that the framework complains if the user tries to add an existing route.
As you can imagine, it is not very difficult to implement. Because we are using a Python dict to store routes, we can simply check if the
given path already exists in the dictionary. If it does, we throw an exception, if it does not we let it add a route.
Before we write any code, let's remember our main `API` class:

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

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."
```

We need to change the `route` function so that it throws an exception if an existing route is being added again:

```python
# api.py

def route(self, path):
    if path in self.routes:
        throw AssertionError("Such route already exists.")

    def wrapper(handler):
        self.routes[path] = handler
        return handler

    return wrapper
```

Now, trying adding the same route twice and restart your gunicorn. You should see the following exception thrown:

```shell
Traceback (most recent call last):
...
AssertionError: Such route already exists.
```

We can refactor it to decrease it to one line:

```python
# api.py

def route(self, path):
    assert path not in self.routes, "Such route already exists."

    ...
```

Voilà! Onto the next feature.

## Class Based Handlers

If you know Django, you know that it supports both function based and class based views (our handlers). We already have function based handlers.
Now we will add class based ones which are more suitable if the handler is more complicated and bigger. Our class based handlers will look like this:

```python
# app.py

@app.route("/book")
class BooksHandler:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

    ...
```

It means that our dict where we store routes `self.routes` can contain both classes and functions as values. Thus, when we find a handler
in the `handle_request()` method, we need to check if the handler is a function or if it is a class. If it is a function, it should work just like now.
If it is a class, depending on the request method, we should call the appropriate method of the class. That is, if the request method is `GET`,
we should call the `get()` method of the class, if it is `POST` we should call the `post` method and etc. Here is how the `handle_request()` method looks like now:

```python
# api.py

def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        handler(request, response, **kwargs)
    else:
        self.default_response(response)

    return response
```

The first thing we will do is check if the found handler is a class. For that, we use the `inspect` module like this:

```python
# api.py

import inspect

...

def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        if inspect.isclass(handler):
            pass   # class based handler is being used
        else:
            handler(request, response, **kwargs)
    else:
        self.default_response(response)

    return response

...
```

Now, if a class based handler is being used, we need to find the appropriate method of the class depending on the request method.
For that we can use the `getattr` built-in function:

```python
# api.py

def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        if inspect.isclass(handler):
            handler_function = getattr(handler(), request.method.lower(), None)
            pass
        else:
            handler(request, response, **kwargs)
    else:
        self.default_response(response)

    return response
```

`getattr` accepts an object instance as the first param and the attribute name to get as the second. The third argument is the value to return if nothing is found.
So, `GET` will return `get`, `POST` will return `post` and `some_other_attribute` will return `None`. If the `handler_function` is `None`, it means
that such function was not method in the class and that this request method is not allowed:

```python
if inspect.isclass(handler):
    handler_function = getattr(handler(), request.method.lower(), None)
    if handler_function is None:
        raise AttributeError("Method now allowed", request.method)
```

If the handler_function was actually found, then we simply call it:

```python
if inspect.isclass(handler):
    handler_function = getattr(handler(), request.method.lower(), None)
    if handler_function is None:
        raise AttributeError("Method now allowed", request.method)
    handler_function(request, response, **kwargs)
```

Now the whole method looks like this:

```python
def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        if inspect.isclass(handler):
            handler_function = getattr(handler(), request.method.lower(), None)
            if handler_function is None:
                raise AttributeError("Method now allowed", request.method)
            handler_function(request, response, **kwargs)
        else:
            handler(request, response, **kwargs)
    else:
        self.default_response(response)
```

I don't like that we have both `handler_function` and `handler`. We can refactor them to make it more elegant:

```python
def handle_request(self, request):
    response = Response()

    handler, kwargs = self.find_handler(request_path=request.path)

    if handler is not None:
        if inspect.isclass(handler):
            handler = getattr(handler(), request.method.lower(), None)
            if handler is None:
                raise AttributeError("Method now allowed", request.method)

        handler(request, response, **kwargs)
    else:
        self.default_response(response)

    return response
```

And that's it. We can now test the support for class based handlers. First, if you haven't already, add this handler to `app.py`:

```python
@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"
```

Now, restart your gunicorn and go to the page `http://localhost:8000/book` and you should see the message `Books Page`. And there you go.
We have added support for class based handlers. Play with them a little bit by implementing other methods such as `post` and `delete` as well.

Onto the next feature!

## Unit Tests

What project is reliable if it has no unit tests, right? So let's add a couple. I like using `pytest`, so let's install it:

```shell
pip install pytest
```

and create a file where we will write our tests:

```shell
touch test_bumbo.py
```

Just to remind you, `bumbo` is the name of the framework. You may have named it differently. Also, if you don't know what [pytest](https://docs.pytest.org/en/latest/) is,
I strongly recommend you look at it to understand how unit tests are written below.

First of all, let's create a fixture for our `API` class that we can use in every test:

```python
# test_bumbo.py
import pytest

from api import API


@pytest.fixture
def api():
    return API()

```

Now, for our first unit test, let's start with something simple. Let's test if we can add a route. If it doesn't throw an exception,
it means that the test passes successfully:

```python

def test_basic_route(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

```

Run the test like this: `pytest test_bumbo.py` and you should see something like the following:

```shell
collected 1 item

test_bumbo.py .                                                                                                                                                            [100%]

====== 1 passed in 0.09 seconds ======
```

Now, let's test that it throws an exception if we try to add an existing route:

```python
# test_bumbo.py

def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO"
```

Run the tests again and you will see that both of them pass.

We can add a lot more tests such as the default response, parameterized routing, status codes and etc. However, all of them require that
we send an HTTP request to our handlers. For that we need to have a test client. But I think this post will become too big if we do it here.
We will do it in the next post in these series. We will also add support for templates and a couple of other interesting stuff. So, stay tuned.

P.S. These blog posts are based on the [Python web framework](https://github.com/rahmonov/alcazar) that I am building. So, [check it out](https://github.com/rahmonov/alcazar) to see
what is yet to come in the blog and make sure to show some love by starring the repo.

Fight on!
