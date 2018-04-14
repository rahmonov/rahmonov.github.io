Title: What is Python?
Date: 2017-10-23 20:10
Modified: 2017-10-23 20:10
Category: python
Tags: python, programming, language
Slug: what-is-python
Authors: Jahongir Rahmonov
Summary: Would you be surprised if I said that Python is not a programming language at all? 

Would you be surprised if I said that Python is not a programming language at all?

Then, let me tell you that Python is actually this guy:

<div class="gallery medium">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/what-is-python/python.jpeg" rel="lightbox" title="Python">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/what-is-python/python.jpeg" alt="Python">
        <span>This is the actual Python</span>
    </a>
</div> 

Just kidding <i class="em em-innocent"></i>. However, even in a programming sense Python is not a language in itself.
It is an *`interface`*. It is basically a description of what a language should do and how it should do it. Don't believe me?
Here is the [official specification](https://docs.python.org/3/reference/) of this interface. Take `if` statements as an example.
Here is what this document says about them:

```commandline
The if statement is used for conditional execution:

if_stmt ::=  "if" expression ":" suite
             ( "elif" expression ":" suite )*
             ["else" ":" suite]
             
It selects exactly one of the suites by evaluating the expressions one by one until one is found to be 
true (see section Boolean operations for the definition of true and false); then that suite is executed 
(and no other part of the if statement is executed or evaluated). If all expressions are false, the 
suite of the else clause, if present, is executed.             
```

"But what have I been using all my life then <i class="em em-astonished"></i>?" I hear you ask. You have been using the default implementation of Python, which is 
actually called *`CPython`*. That means that by *`Python`* most people mean *`CPython`*. Read on to understand what that is.

As with any `interface`, there are its implementations. And the most popular Python implementations are the following:

1. [CPython](https://github.com/python/cpython) - The default and most widely used implementation written in C
2. [Jython](http://www.jython.org/) - Written in Java and for the JVM
3. [IronPython](http://ironpython.net/) - Written in C# and tightly integrated with the .NET framework.
4. [PyPy](https://pypy.org/) - Alternative implementation of Python written in (surprise!) Python.

And here is the most interesting part: as these implementations are written in different languages, they allow you to use them inside
your Python program. Specifically, `CPython` allows to use `C` and `C++`, `Jython` allows to use `Java` and `IronPath` allows to use 
`C#` in your Python program.  How crazy is that? 
 
Let's see some examples. Let's say that I have this function called `example` written in `C`:
 
```cython
static PyObject * example(PyObject *self)
{
    // do something
    return Py_BuildValue("i", result);
}
``` 

In `CPython`, I can import it and call it like this:

```python
import example

result = example.do_something()
```

These are called extensions. Read more about them [here](https://docs.python.org/3/extending/extending.html).

The same thing with `Jython`. You can import `Java` classes and use them inside your Python:

```python
C:\jython>jython
Jython 2.0 on java1.2.1
Type "copyright", "credits" or "license" for more information.
>>> from java.util import Random
>>> r = Random()
>>> r.nextInt()
-790940041
```

And the same thing with `IronPython`. Import `.NET` code and use it as you like:

```python
>>> from System.DateTime import Now
>>> Now #doctest: +ELLIPSIS
<System.DateTime object at ...>
>>> # Let's make it even more obvious that "Now" is evaluated only once
>>> a_second_ago = Now
>>> import time
>>> time.sleep(1)
>>> a_second_ago is Now
True
>>> a_second_ago is System.DateTime.Now
False
```

I don't know about you but mixing up languages like this is fascinating to me, although I haven't had a chance to use any of them
in a real project except for `CPython`, of course.
 
However, that might be not too far away. Hailed as the future of Python, `PyPy` has been showing great progress. Even the creator of Python,
Guido van Rossum said some nice words about it:
 
> If you want your code to run faster, you should probably just use PyPy.
 
Its distinctive features, apart from being fast thanks to its Just-in-Time compiler, include optimized memory usage, support for stackless
which makes massive concurrency possible and most importantly its compatibility. That means that you can swap your Python implementation with 
`PyPy` without changing your codebase and you will have all those advantages that `PyPy` offers. You can read more about its 
features [here](https://pypy.org/features.html).

## Conclusion
Python is actually an interface and there are several different implementations, with the most commonly used being `CPython` and 
most promising being `PyPy`. Thank you for reading!

Fight on!
