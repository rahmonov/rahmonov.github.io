Title: Custom ChainMap in Python
Date: 2017-10-19 20:10
Modified: 2017-10-19 20:10
Category: programming
Tags: python, collections, chainmap
Slug: custom-chainmap-in-python
Authors: Jahongir Rahmonov
Summary: Custom implementation of Python's standard ChainMap

In [the previous post](/posts/python-chainmap/), we learned what `ChainMap` is in Python and how/why to use it. In this blog
post, we will awaken our inner hacker and try to implement the same thing ourselves. Just for fun :) Please, check out 
[this post](/posts/python-chainmap/) if you don't know what `ChainMap` is.

As software developers, we often hear the words "Don't reinvent the wheel" which basically means "Don't recreate basic stuff which
has been created before for you". However, I believe that occasional reinventions of some "wheels" help us understand some things
from the inside out and grow as software developers.

So, let's go ahead and reinvent `ChainMap` in Python.

First things first, let's do the initialization process. The original version takes an undefined number of dictionaries upon initialization 
and store them inside the `maps` property:

```python
>>> from collections import ChainMap

>>> a = {'name': 'hell', 'value': 'yeah'}
>>> b = {'name': 'paradise', 'value': 'no'}

>>> first_chain = ChainMap(a)
>>> print(first_chain.maps)
[{'value': 'yeah', 'name': 'hell'}]
>>> second_chain = ChainMap(a, b)
>>> print(second_chain.maps)
[{'value': 'yeah', 'name': 'hell'}, {'value': 'no', 'name': 'paradise'}]
>>> third_chain = ChainMap()
>>> print(first_chain.maps)
[{}]
```

Based on these observations, we can conclude that we should override the `__init__` method and it should take a number of dictionaries and store them in
`maps` property which is a list. If no dictionary is given, `maps` should be equal to a list of one empty dict:

```python
class MyChainMap:
    def __init__(self, *maps):
        self.maps = list(maps) or [{}]
        
    def get(self, key, default=None):
        for map in self.maps:
            if key in map:
                return map[key]
                
        return default
```

`maps` should be converted to list because `*maps` is a tuple. Let's try it out:

```python
>>> my_chain = MyChainMap(a, b)
>>> print(my_chain.maps)
[{'name': 'hell', 'value': 'yeah'}, {'name': 'paradise', 'value': 'no'}]
```

Great! Next, let's do the `get()` method. In the original version, `get` takes two parameters: `key` and `default=None`. It tries
to find the key and returns the value if found. Otherwise, it returns the `default` (whose default is `None`):

```python
>>> print(first_chain.get('name'))
'hell'
>>> print(first_chain.get('nonexistent_key') is None)
True
>>> print(first_chain.get('nonexistent_key', 'default_value'))
'default_value'
```

We will try to find the given key in our `maps` and return the first found result, otherwise we will return the default value:

```python
class MyChainMap:
    ...
    
    def get(self, key, default=None):
        for map in self.maps:
            if key in map:
                return map[key]
                
        return default
```

Let's try it out:

```python
>>> my_chain = MyChainMap(a, b)
>>> print(my_chain.get('name'))
'hell'
>>> print(my_chain.get('nonexistent_key') is None)
True
>>> print(my_chain.get('nonexistent_key', 'default_value'))
'default_value'
```

Works and looks the same. Great! We know that in the original `ChainMap`, we can retrieve values just like dicts:

```python
>>> first_chain['name']
'hell'
>>> first_chain['nonexistent_key']
KeyError: 'nonexistent_key'
```

It returns the value if found, otherwise throws `KeyError`. From Python's data model, we know that the special `__getitem__` method 
is called when accessing a key like a dict: `first_chain['name']`. So, we will override it accordingly:

```python
class MyChainMap:
    ...
    
    def __getitem__(self, key):
        for map in self.maps:
            if key in map:
                return map[key]
                
        raise KeyError(key)
```

Let's try it out:

```python
>>> my_chain = MyChainMap(a, b)
>>> my_chain['name']
'hell'
>>> my_chain['nonexistent_key']
KeyError: 'nonexistent_key'
```

Very nice! 

Next, let's implement the `new_child` method of `ChainMap`. As we know, it takes one dictionary as a parameter and returns a new object with
whose `maps` consists of this new dictionary and its other dictionaries:

```python
class MyChainMap:
    ... 
    
    def new_child(self, new_map):
        return MyChainMap(new_map, *self.maps)
```

So, we just initialized a new object with the new map and old ones. Easy! Let's try it out:

```python
>>> my_chain = MyChainMap(a)
>>> my_new_chain = my_chain.new_child(b)
>>> my_new_chain.maps
[{'name': 'paradise', 'value': 'no'}, {'name': 'hell', 'value': 'yeah'}]
```

Great! And lastly, let's implement the `parents` property of the `ChainMap`. We know that it returns a new `ChainMap` with all the maps
except for the first one. So, it should be pretty easy as well:

```python
class MyChainMap:
    ... 
    
    @property
    def parents(self):
        return MyChainMap(*self.maps[1:])
```

and there you go! Please note that it is a property not a callable function, just like in the original implementation. Let's try it out:

```python
>>> a = {'name': 'hell', 'value': 'yeah'}
>>> b = {'name': 'paradise', 'value': 'no'}

>>> my_chain = MyChainMap(a, b)
>>> print(my_chain.maps)
[{'value': 'yeah', 'name': 'hell'}, {'value': 'no', 'name': 'paradise'}]
>>> chain_parents = my_chain.parents
>>> print(chain_parents.maps)
[{'value': 'no', 'name': 'paradise'}]
```

Awesome! And there you have it. A custom version of `ChainMap`. But it is not yet complete. I will leave the rest of it up to you <i class="em em-innocent"></i>.

Go ahead and try to implement `pop`, `clear`, `__setitem__` and `__delitem__` methods of `ChainMap` and let me know in the comments if you did or have any questions.

Be a hacker and fight on!

