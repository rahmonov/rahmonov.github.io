Title: Python Decorators
Date: 2017-08-30 20:10
Modified: 2017-08-30 20:10
Category: programming
Tags: python, decorators, function
Slug: python-decorators
Authors: Jahongir Rahmonov
Summary: A tale of decorators in Python

The following is a tale of how one programmer learned the basics of decorators in Python and is told from his point of view.

## The Tale
So, my boss told me to write two functions both of which return whatever they accept. Well, that seems pretty easy:

```python
def first_func(arg):
    return arg

def second_func(arg):
    return arg
```
        
When I asked him what the difference was between these two functions he said that the first one should only accept integers and
the second one should only accept strings, otherwise they both should raise an `AssertionError` with a helpful message.

Okay, that should not be too difficult:

```python
def first_func(arg):
    assert isinstance(arg, int), "{arg} is not an instance of int".format(arg=arg)
    return arg
    
def second_func(arg):
    assert isinstance(arg, str), "{arg} is not an instance of str".format(arg=arg)
    return arg
```
        
Let's try them out:

```python
>>> first_func(123)
>>> 123

>>> first_func('some text')
---------------------------------------------------------------------------
AssertionError: some text is not an instance of int

>>> second_func('text')
>>> 'text'

>>> second_func(123)
---------------------------------------------------------------------------
AssertionError: 123 is not an instance of str
```
    
Cool, they seem to work pretty well. But it bothers me that those assertion lines seem exactly the same and I am not following
the DRY principle. Uncle Bob will kill me. I think I should probably factor them out to a separate function and call where needed.
The function should accept an argument and a type and check if that argument is an instance of that type. If not, raise an assertion error:

```python
def assert_type(arg, type):
    assert isinstance(arg, type), "{arg} is not an instance of {type}".format(arg=arg, type=type)
```
        
Now I can call this in the two functions that I wrote earlier:

```python
def first_func(arg):
    assert_type(arg, int)
    return arg
    
def second_func(arg):
    assert_type(arg, str)
    return arg
```
 
Looks much better now and they are producing the same results. Hmmm, I have a strange feeling that I could improve this further. 
It is Python after all. There should be something more pythonic. As [Raymond Hettinger](https://twitter.com/raymondh) would say:
 
<div class="gallery medium">
    <a href="/static/images/post-images/python-decorators/raymondhettinger.jpg" rel="lightbox" title="Raymond Hettinger">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/python-decorators/raymondhettinger.jpg" alt="Raymond Hettinger">
        <span>There must be a better way!</span>
    </a>
</div> 
 
I need to do a little research on how I can accomplish this feat.
 
    ...after 3 days...
 
Oh wow! I watched this [amazing talk by James Powell](https://www.youtube.com/watch?v=7lmCu8wz8ro) and learned that there is a feature
in Python that does exactly what I want to do with my functions and it is called `decorators` <i class="em em-tada"></i>

Basically, what they allow me to do is add an additional functionality to my existing functions. That's exactly what I want to do: I want
to add type-checking functionality to my existing `first_func` and `second_func`. Let's see an example:

```python
def p_decorate(func):
   def func_wrapper(name):
       return "<p>{0}</p>".format(func(name))
   return func_wrapper

@p_decorate
def get_text(name):
   return "lorem ipsum, {0} dolor sit amet".format(name)
```
   
 
So, in this example, there is a `get_text` function which accepts a parameter `name` and returns a string of that name inside a random text.
There is another method called `p_decorate`. It accepts a function and returns a function which is declared inside this `p_decorate`. It accepts
`name` as a parameter. It then surrounds it with `<p></p>` tags and returns the result. And one more thing to note is that there is
`@p_decorate` on top of `def get_text(name)`.
  
This is all very mysterious to me but let's see what result it will yield:
  
```python
>>> get_text('John')
>>> '<p>lorem ipsum, John dolor sit amet</p>'
```
    
Okay, the expected result. Let's try to understand what is going on here:
    
First, when I call `get_text`, it will actually call `p_decorate(get_text)` because of `@p_decorate` on top of the function declaration.
And what will `p_decorate(get_text)` return? It will return another function called `func_wrapper`. So, basically 
`get_text(name)` will be replaced by `func_wrapper(name)` which will return `p` tag surrounded string that we saw.

Now, it is much clearer to me. Back to my own functions. 

Using these decorators, I want my end result to look like this:

```python
@assert_type(int)
def first_func(arg):
    return arg
```
            
It means that our decorator will have one more layer which will accept the type as parameter and will have two inner functions. Let's 
try to write that decorator:

```python
def assert_type(type):
    def wrapper(func):
        def decorated_func(arg):
            assert isinstance(arg, type), "{arg} is not an instance of {type}".format(arg=arg, type=type)
            return func(arg)
            
        return decorated_func
        
    return wrapper
```
        
Cool! And now I can use this decorator as I wanted:

```python
@assert_type(int)
def first_func(arg):
    return arg
    
@assert_type(str)
def second_func(arg):
    return arg
```
        
and run some tests:
        
```python
>>> first_func(123)
>>> 123
>>> first_func('123')
---------------------------------------------------------------------------
AssertionError: 123 is not an instance of <class 'int'>
```

Voila! It is working as before but now the functions are much better-looking. They are even hot <i class="em em-fire"></i><i class="em em-heart_eyes"></i>

Wow! I could not even imagine that I would learn so much more than just the decorators. 

Along the way, I learned that functions are [first-class objects](https://dbader.org/blog/python-first-class-functions) in Python which means that I can use a function as arguments to another function:

```python
>>> def add(x, y):
        return x + y
        
>>> def apply(func, x, y):
        return func(x, y)
```

I also learned that functions can have [inner functions](http://www.devshed.com/c/a/python/nested-functions-in-python/):

```python
def assert_type(type):
    def wrapper(func):
        def decorated_func(arg):
            assert isinstance(arg, type), "{arg} is not an instance of {type}".format(arg=arg, type=type)
            return func(arg)
            
        return decorated_func
        
    return wrapper
```
        
And most importantly those inner functions can use the variables from the outer functions and can remember them even when 
they go out of scope ([clojure](https://www.programiz.com/python-programming/closure)), like in the following line:

```python
assert isinstance(arg, type), "{arg} is not an instance of {type}".format(arg=arg, type=type)
```
    
where `type` comes from the function above.

Overall, it was a productive day <i class="em em-sunglasses"></i>

## Conclusion
Thanks for reading thus far. This post was not written to illustrate what exactly decorators are or how they work. But rather, it was
written in order to show why we need decorators and how they can improve our code. That's why, in order to make your decorators knowledge
comprehensive, please go ahead and read the [these](http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/) 
[blog posts](https://www.thecodeship.com/patterns/guide-to-python-function-decorators/) for details. They are awesome!

P.S. There is the complementary video that I have made on Python Decorators :)

<iframe width="560" height="315" src="https://www.youtube.com/embed/IJTwV548Qn0" frameborder="0" allowfullscreen></iframe>

Fight on!