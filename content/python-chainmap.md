Title: Python ChainMap
Date: 2017-10-17 20:10
Modified: 2017-10-17 20:10
Category: programming
Tags: python, collections, chainmap
Slug: python-chainmap
Authors: Jahongir Rahmonov
Summary: The comprehensive guide to Python's collections module. Part Two: ChainMap

In [Part I](/posts/python-collections-counter/) of these series about Python's collections module, we talked about the
`Counter` class and its usage. In this blog post, we will be looking at another class in this module: `ChainMap`.

Let's say that we are building this awesome web app which is expected to bring us billions of dollars. In this app, we have
two environments: development and production. Each of these environments has its own configurations and we store 
those configs in dictionaries, like this:
 
```python
development = {'app_name': 'Billions', 'database': '132.123.33.2', 'db_username': 'development_user'}

production = {'database': '222.44.55.16', 'db_username': 'production_user'}
``` 

When deploying our app in production, we first look up the `production` dictionary for a value. If nothing is found, then 
we look it up from the `development` dictionary. Nothing new, classic config; production overrides development.
 
To do that, let's create a function called `get_config`, which takes `name` as a parameter and returns the result if it finds it, or else `None`:
 
```python
>>> def get_config(name):
...     if name in production:
...         return production[name]
...        
...     if name in development:
...         return development[name]
...        
...     return None
```

Let's test it:

```python
>>> get_config('database')
'222.44.55.16'
>>> get_config('db_username')
'production_user'
>>> get_config('app_name')
'Billions'
>>> get_config('api_key') is None
True
```
 
Looks like it is working well. Please note that this method is for production only. In development, we would first search in the `development` dict and only
then `production`.
  
This is working well, but I don't like it. There has to be a better way. What if I combine them in one dict? Like this:
   
```python
>>> development = {'app_name': 'Billions', 'database': '132.123.33.2', 'db_username': 'development_user'}
>>> production = {'database': '222.44.55.16', 'db_username': 'production_user'}
>>>
>>> common = dict()
>>> common.update(development)
>>> common.update(production)
```   

Looks good. Let's test it:

```python
>>> common.get('database')
'222.44.55.16'
>>> common.get('db_username')
'production_user'
>>> common.get('app_name')
'Billions'
>>> common.get('api_key') is None
True
```

Cool! It is behaving in the same way as the method we wrote above. However, we did it without having to write a function.

Well, it turns out that there is even better way. Welcome [ChainMap](https://docs.python.org/3/library/collections.html#chainmap-objects)!

Basically, what it does is to group multiple dicts into one, updateable view which has the same interface as the ordinary dict (with some additions, of course).
Let's see it in action:

```python
>>> from collections import ChainMap
>>>
>>> development = {'app_name': 'Billions', 'database': '132.123.33.2', 'db_username': 'development_user'}
>>> production = {'database': '222.44.55.16', 'db_username': 'production_user'}
>>>
>>> chain = ChainMap(production, development)
>>>
>>> chain.get('database')
'222.44.55.16'
>>> chain.get('db_username')
'production_user'
>>> chain.get('app_name')
'Billions'
>>> chain.get('api_key') is None
True
```

Awesome! Look how much cleaner it got. With one single line, we accomplished all those things that we did above.

## Other Features

As I mentioned above, it looks and behaves just like an ordinary dict. However, it has some extra functionality.

You can see the list of comprising dictionaries:

```python
>>> chain.maps
[{'database': '222.44.55.16', 'db_username': 'production_user'}, {'database': '132.123.33.2', 'db_username': 'development_user', 'app_name': 'Billions'}]
```

You can reverse this order:

```python
>>> chain.maps = list(reversed(chain.maps))
>>> chain.maps
[{'database': '132.123.33.2', 'db_username': 'development_user', 'app_name': 'Billions'}, {'database': '222.44.55.16', 'db_username': 'production_user'}]
```

This means that now when look something up, it will first loop up the `development` dictionary because we reversed the order:

```python
>>> chain.get('db_username')
'development_user'
```

Cool! 

You can also add another dictionary to the group:

```python
>>> most_important_config = {'db_username': 'I am the king'}
>>> chain = chain.new_child(most_important_config)
>>> chain.get('db_username')
'I am the king'
```

As you can see, the one we just added was added as the first child and thus it will look it up first.

And lastly, you can see `parents` of this chain which basically means see all comprising dictionaries except the first one:

```python
>>> >>> chain.parents
ChainMap({'database': '132.123.33.2', 'db_username': 'jahongirr', 'app_name': 'Billions'}, {'database': '222.44.55.16', 'db_username': 'production_user'})
```

As you can see here, contents of `most_important_config` is missing as it is the first element of the `ChainMap`.

## Conclusion
In this blog post, we saw what `ChainMap` is, how to use it and most importantly why to use it. Always learn why something should be used.
Otherwise, it is easy to forget or misuse it.

Fight on!
