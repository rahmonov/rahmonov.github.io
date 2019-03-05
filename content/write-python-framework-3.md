Title: How to write a Python web framework. Part III.
Date: 2019-03-03 20:10
Modified: 2019-03-03 20:10
Category: python
Tags: programming, python
Slug: write-python-framework-part-three
Authors: Jahongir Rahmonov
Summary: The third post of the series where we will be writing our own Python framework just like Flask and Django.

*Check out Part I [here](/posts/write-python-framework-part-one/)*<br>
*Check out Part II [here](/posts/write-python-framework-part-two/)*

> A little reminder that this series is based on the [Alcazar framework](https://github.com/rahmonov/alcazar) that I am writing for
learning purposes. If you liked this series, show some love by starring the [repo](https://github.com/rahmonov/alcazar).

In the previous blog posts in the series, we started writing our own Python framework and implemented
the following features:

- WSGI compatible
- Request Handlers
- Routing: simple and parameterized
- Check for duplicate routes
- Class Based Handlers
- Unit tests

In this part, we will add a few awesome features to the list:

- Test Client
- Alternative way to add routes (like Django)
- Support for templates

## Test Client

In the [part 2](/posts/write-python-framework-part-two/), we wrote a couple of unit tests. However, we stopped when we needed to
send HTTP requests to our handlers because we didn't have a test client that could do that. Let's add one then.

By far the most popular way of sending HTTP requests in Python is the [`Requests`](https://github.com/kennethreitz/requests) library by [Kenneth Reitz](https://twitter.com/kennethreitz).
However, for us to be able to use it in the unit tests, we should always have our app up and running (i.e. start gunicorn before running tests). The reason
is that [Requests only ships with a single Transport Adapter, the HTTPAdapter](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters).
That defeats the purpose of unit tests. Unit tests should be self sustained. Fortunately for us, [Sean Brant](https://github.com/seanbrant) wrote a
[WSGI Transport Adapter for Requests](https://github.com/seanbrant/requests-wsgi-adapter) that we can use to create a test client.
Let's write the code first and then discuss.

Add the following method to the main `API` class in `api.py`:

```python
# api.py
...
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter


class API:
    ...

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    ...

```

As written [here](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters), to use the Requests WSGI Adapter,
we need to mount it to a Session object. This way, any request made using this `test_session` whose URL starts with the given prefix will use the given RequestsWSGIAdapter.
Great, now we can use this `test_session` to create a test client. Create a `conftest.py` file and move the `api` fixture to this file so that it looks like this:

```python
# conftest.py
import pytest

from api import API


@pytest.fixture
def api():
    return API()
```

In case you didn't know, this file is where `pytest` looks for fixtures by default. Now, let's create the test client fixture here:

```python
# conftest.py
...

@pytest.fixture
def client(api):
    return api.test_session()
```

Our `client` needs the `api` fixture and returns the `test_session` that we wrote earlier. Now we can use this `client` fixture in our unit tests.
Let's go right ahead to the `test_bumbo.py` file and write a unit test that tests if the `client` can send a request:

```python
# test_bumbo.py
...

def test_bumbo_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT
```

Run the unit tests by `pytest test_bumbo.py` and voila. We see that all the tests pass. Let's add a couple more unit tests for the most important parts:

```python
# test_bumbo.py
...

def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"
```

This tests that the parameters that we send in the url are working.

```python
# test_bumbo.py
...

def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found."
```

This one tests that if a request is sent to a non existent route, 404(Not Found) response is returned.

The rest I will leave to you. Try to write a couple more tests and let me know in the comments if you need any help. Here are some ideas for unit tests:

- test that class based handlers are working with a GET request
- test that class based handlers are working with a POST request
- test that class based handlers are returning `Method Not Allowed.` response if an invalid request method is used
- test that status code is being returned properly

## Alternative way to add routes

Right now, here is how routes are added:

```python

@api.route("/home")
def handler(req, resp):
    resp.text = "YOLO"

```

That is, routes are added as decorators, like in Flask. Some people may like the Django way of registering urls. So, let's give them a choice to add routes like this:

```python
def handler(req, resp):
    resp.text = "YOLO"


def handler2(req, resp):
    resp.text = "YOLO2"

api.add_route("/home", handler)
api.add_route("/about", handler2)
```

This `add_route` method should do two things. Check if the route is already registered or not and if not, register it:

```python
# api.py

class API:
    ...

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler
```

Pretty simple. Does this code look familiar to you? It is because we already wrote such code in the `route` decorator. We can now follow the DRY principle and
use this `add_route` method inside the `route` decorator:

```python
# api.py


class API:
    ...

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler

    def route(self, pattern):
        def wrapper(handler):
            self.add_route(pattern, handler)
            return handler

    return wrapper

```

And let's add a unit test to check if it is working:

```python
# test_bumbo.py

def test_alternative_route(api, client):
    response_text = "Alternative way to add a route"

    def home(req, resp):
        resp.text = response_text

    api.add_route("/alternative", home)

    assert client.get("http://testserver/alternative").text == response_text
```

Run your tests and you will see that all of them pass.

## Templates support

When I am implementing something new, I like to do something called README driven development. It is a technique where you write down
how you want your API to look like before implementing. Let's do just that for this feature. Say we have this template that we want to use in our handler:

```html
<html>
    <header>
        <title>{{ title }}</title>
    </header>

    <body>
        The name of the framework is {{ name }}
    </body>

</html>
```

`{{ title }}` and `{{ name }}` are variables that are sent from a handler and here is how a handler looks like:

```python

api = API(templates_dir="templates")

@api.route("/home")
def handler(req, resp):
    resp.body = api.template("home.html", context={"title": "Awesome Framework", "name": "Alcazar"})
```

I want it to be as simple as possible so I just need one method that takes template name and context as params and
renders that template with the given params. Also, we want templates directory to be configurable just like above.

With the API designed, we can now implement it.

For templates support, I think that [Jinja2](http://jinja.pocoo.org/docs/2.10/) is the best choice. It is a modern and designer-friendly templating language for Python, modelled after Django’s templates.
So, if you know Django it should feel right at home.

`Jinja2` uses a central object called the template `Environment`. We will configure this environment upon application initialization and load templates with the help of this environment.
Here is how to create and configure one:

```python
from jinja2 import Environment, FileSystemLoader

templates_env = Environment(loader=FileSystemLoader(os.path.abspath("templates")))
```

`FileSystemLoader` loads templates from the file system. This loader can find templates in folders on the file system and is the preferred way to load them.
It takes the path to the templates directory as a parameter. Now we can use this `templates_env` like so:

```python
templates_env.get_template("index.html").render({"title": "Awesome Framework", "name": "Alcazar"})
```

Now that we understand how everything works in `Jinja2`, let's add it to our own framework. First, let's install `Jinja2`:

```shell
pip install Jinja2
```

Then, create the `Environment` object in the `__init__` method of our `API` class:

```python
# api.py
from jinja2 import Environment, FileSystemLoader


class API:
    def __init__(self, templates_dir="templates"):
        self.routes = {}

        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))

    ...
```

We did almost the same thing as above except that we gave `templates_dir` a default value of `templates` so that users don't
have to write it if they don't want to. Now we have everything to implement the `template` method we designed earlier:

```python
# api.py

class API:
    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)
```

I don't think there is a need to explain anything here. The only thing you may wonder about is why I gave `context` a default value of `None`,
checked if it is `None` and then set the value to an empty dictionary `{}`. You may say I could have given it the default value of `{}` in the declaration.
But `dict` is a mutable object and it is a bad practice to set a mutable object as a default value in Python. Read more about this [here](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments).

With everything ready, we can create templates and handlers. First, create the `templates` folder:

```shell
mkdir templates
```

Create the `index.html` file by doing `touch templates/index.html` and put the following inside:

```html
<html>
    <header>
        <title>{{ title }}</title>
    </header>

    <body>
        <h1>The name of the framework is {{ name }}</h1>
    </body>

</html>
```

Now we can create a handler in our `app.py`:

```python
# app.py

@api.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", context={"name": "Alcazar", "title": "Best Framework"})
```

That's it (well, almost). Start `gunicorn` and go to `http://localhost:8000/template`. You will see a big bold `Internal Server Error`.
That's because `resp.body` expects bytes and our `template` method returns a unicode string. Thus, we will need to encode it:

```python
# app.py

@api.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", context={"name": "Alcazar", "title": "Best Framework"}).encode()
```

Restart gunicorn and you will see our template in all its glory. In the future posts, we will remove the need to `encode` and make our
API prettier.

## Conclusion

We have implemented three new features in this post:

- Test Client
- Alternative way to add routes (like Django)
- Support for templates

Make sure to let me know in the comments what other features we should implement in this series. For the next part, we will definitely add
support for static files but I am not sure what other features we should add.

*Check out Part I [here](/posts/write-python-framework-part-one/)*<br>
*Check out Part II [here](/posts/write-python-framework-part-two/)*

> A little reminder that this series is based on the [Alcazar framework](https://github.com/rahmonov/alcazar) that I am writing for
learning purposes. If you liked this series, show some love by starring the [repo](https://github.com/rahmonov/alcazar).

That's it for today!

Fight on!