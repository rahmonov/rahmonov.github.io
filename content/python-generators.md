Title: Python Generators
Date: 2017-09-02 20:10
Modified: 2017-09-02 20:10
Category: programming
Tags: python, generators, function
Slug: python-generators
Authors: Jahongir Rahmonov
Summary: A tale of generators in Python

This is a tale of how one programmer learned the basics of generators in Python and is told from his point of view.
 
## The Tale
So, my boss told me to write a function that accepts `n` as a parameter and generates this many random numbers and returns the result.
That should not be too difficult:
 
```python
import random

def random_nums(n):
    nums = []
    for i in range(n):
        nums.append(random.randint(0, 1000))   # random number is between 0 and 1000
    return nums
``` 

Let me test it out:

```python
>>> random_nums(10)
[886, 348, 763, 493, 401, 219, 911, 789, 834, 940]

>>> random_nums(5)
[366, 160, 951, 682, 153]
```

It seems to be working well. However, I have a few concerns about this function. First of all, what if the `n` param is really large?
Because the function stores the random numbers in a list (`nums = []`), that list will get bigger and bigger, and eventually the machine may run
out of memory.

Second of all, the function is *eager* which means that it will go from the start till the end without any pause. This, in turn, means that
if I want to do something like this:
 
```python
for i in random_nums(10000000):
    print(i)
```

It will first execute `random_nums(10000000)` part and then start the loop. It means that even if I needed only the first element of the list, I would
have to wait for all 10000000 numbers to be generated. That sucks <i class="em em-confounded"></i>

<div class="gallery large">
    <a href="/static/images/post-images/python-generators/large_number.gif" rel="lightbox" title="Large Number">
        <img src="/static/images/post-images/python-generators/large_number.gif" alt="Large Number">
        <span>Waiting for the first number...</span>
    </a>
</div> 

Well, there must be a better way. There must be a solution which solves both memory and eagerness issues. So, in order to achieve that
I must get rid of storing the numbers and make the function lazy so that it generates one number at a time. What if I create such a class?
That should not be too difficult. I could use `__iter__` and `__next__` functions to make my class iterable and in that `__next__` I will return
one number at a time and remember the last index:
 
```python
class BetterRandomNums:
    def __init__(self, n):
        self.n = n
        self.index = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        random_number = random.randint(0, 1000)
        
        if self.index >= self.n:
            raise StopIteration('No more numbers')
            
        self.index += 1
        
        return random_number
``` 

Let me try it out now:

<div class="gallery large">
    <a href="/static/images/post-images/python-generators/better-random.gif" rel="lightbox" title="Better random generator">
        <img src="/static/images/post-images/python-generators/better-random.gif" alt="Better random generator">
        <span>Better random number generator</span>
    </a>
</div> 

Now, it is better! Basically, it is generating one random number, giving me that number and letting me print it and only then going on
to create the next random number. Exactly what I wanted <i class="em em-tada"></i>

Now, if I try to access the first number, it will happen immediately:

<div class="gallery large">
    <a href="/static/images/post-images/python-generators/fast-first-number.gif" rel="lightbox" title="Fast First Number">
        <img src="/static/images/post-images/python-generators/fast-first-number.gif" alt="Fast First Number">
        <span>Fast access to the first number</span>
    </a>
</div>

There you go. This is what I wanted to do. But boy does it look ugly and I can't believe that I had to do all these things to get this done.
This is Python, there must be a Pythonic way of doing it.

    After doing a little research...
   
Hooray! It turns out there is such a thing and it is called `generators` <i class="em em-star2"></i>

Using a generator, our new function will look like this vs the old one:

```python
# the new function                                            # the old one
def random_nums2(n):                                |         def random_nums(n):
    for i in range(n):                              |            nums = []    
        rand_num = random.randint(0, 1000)          |            for i in range(n):
                                                    |                nums.append(random.randint(0, 1000))
        yield rand_num                              |            return nums
```

So, what changed? They look very similar. The are two small differences, though. First, the new function does not store the results in a list.
That's why, it will not use any memory for that. Second, instead of `return` we have `yield`. This is the **keyword** that turns a function
into a generator. As a result, it will generate a random number, give a user that random number, and then that's it; it will remember that it 
produced one random number and wait for the user to continue. Only when the user calls it again, it will generate the second random number. 

Let's try it out:

<div class="gallery large">
    <a href="/static/images/post-images/python-generators/generator.gif" rel="lightbox" title="Generator">
        <img src="/static/images/post-images/python-generators/generator.gif" alt="Generator">
        <span>Generator at work</span>
    </a>
</div>

Basically, it is working just like the `BetterRandomNums` class above. But it is much more compact and does not require knowledge of all those
magic methods that the class had. As PewDiePie would say:

<div class="gallery medium">
    <a href="/static/images/post-images/python-generators/very-nice.jpg" rel="lightbox" title="Very nice">
        <img src="/static/images/post-images/python-generators/very-nice.jpg" alt="Very nice">
        <span>Very nice</span>
    </a>
</div>

## Conclusion
There you have it. We had problems of memory and an eager function. We solved them with the help of generators. This tale was intended to show 
not only how to use generators but also why we need to use them. I hope it is more or less clear. If not, [contact me](/pages/about.html#contact) 
and I will do my best to explain things further.

Thanks for reading and fight on!