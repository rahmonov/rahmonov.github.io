Title: Python GIL
Date: 2017-12-08 20:10
Modified: 2017-12-08 20:10
Category: programming
Tags: python
Slug: python-gil
Authors: Jahongir Rahmonov
Summary: What is the Global Interpreter Lock in Python?

Let's say that we want to write a function that takes a number as an argument and simply counts down. Pretty easy:

```python
def count_down(n):
    while n > 0:
        n -= 1
```

Let's call this function with a big number and measure how much it takes:

```python
from time import time

before = time()
count_down(100000000)
after = time()

print(after-before)
```

On my machine, it takes 8.54 seconds. Now, let's call it twice and measure that:

```python
from time import time

before = time()
count_down(100000000)
count_down(100000000)
after = time()

print(after-before)
```

On my machine, it takes 17.38 seconds. 

It is working fine but our boss is not happy. He wants us to make it faster. How do we make it faster? We use threads so
that these two function calls run in parallel, right? In theory, running a function twice in parallel should take as much as running 
it once. Because, well, those two function calls run in parallel. Let's try this out by calling the function twice but in different threads:

```python
from threading import Thread
from time import time

before = time()

thread1 = Thread(target=count_down, args=(100000000,))
thread2 = Thread(target=count_down, args=(100000000,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

after = time()
print(after-before)
```

It takes around 18.4 seconds on my machine. Wait, WHAT? <i class="em em-astonished"></i> It not only did not take as much as calling the function once
but in fact it was even slower than calling the function twice without Threads. Try that with Python2.7 and you will get even worse results. 
A prominent software developer, David Beazly reported that it even took almost 2x time in his talk [Inside the Python GIL](http://www.dabeaz.com/python/GIL.pdf).
  
## But, WHY? 
 
Please, welcome the notorious GIL - Global Interpreter Lock. This guy is to blame for all the problems in the world. GIL allows only 
one thread to run at a time. In the above example, when we thought we were using two threads, we were only using just one, because the big boss 
GIL did not allow us to. That's why, it did not run faster. But, why was it even slower? That's because every now and then Python 
tries to switch Threads as we asked him to use two. GIL does not allow him to do so. However, when he tries to switch to no avail, there is 
some overhead associated with it. Thus, the end result is even slower.

## But, WHY? 

We all know that Threads can be a good thing and help us make our programs run much faster. Why does the GIL exist, then? Damn you, GIL! 
You are like Negan from the Walking Dead. 

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/python-gil/negan.jpg" rel="lightbox" title="Negan - GIL">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/python-gil/negan.jpg" alt="Negan - GIL">
        <span>Negan - GIL</span>
    </a>
</div>

Well, it turns out GIL is not the villain after all. Actually, GIL is the good guy. It turns out that Python's memory management is not 
thread-safe! That is, if you run multiple threads, your program may behave in weird and even catastrophic ways. GIL is there to help us from such 
scenarios.

<div class="gallery large">
    <a href="https://s3.amazonaws.com/rahmonov.me/post-images/python-gil/superman.jpg" rel="lightbox" title="Superman - GIL">
        <img src="https://s3.amazonaws.com/rahmonov.me/post-images/python-gil/superman.jpg" alt="Superman - GIL">
        <span>Superman - GIL</span>
    </a>
</div>

## But, wouldn't it be easier to remove the Thread class instead?

Excellent question! Instead of writing an additional tool that would prevent Threads from doing bad things to our programs, why not just 
delete the `Thread` classes so that programmers simply won't be able to use them? We are not allowed to use them anyways.

Turns out, there are some cases when `Thread` can be of use. All above examples were CPU bound, meaning that they need only CPU to run, they wait on CPU. 
However, if your code is IO bound or image processing or NumPy number crunching, GIL won't be in your way as these operations happen outside 
the GIL. That's where you can use the `Thread` class safely and effectively.
 
Let's write some IO bound function. A function that requests a web url and returns its content as a text:
 
```python
import requests

def get_content(url):
    response = requests.get(url)
    return response.text
``` 
  
Calling this function once with the argument `https://google.com` takes 0.88 seconds on my machine. Calling it twice - 1.72 seconds, of course.
Now, let's call it twice in different threads and see the `Thread`'s effect:
  
```python
before = time()

thread1 = Thread(target=get_content, args=('https://google.com',))
thread2 = Thread(target=get_content, args=('https://google.com',))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

after = time()

print(after - before)
```  
  
It takes 0.89 seconds. Hooray! Calling the function twice in different threads took as much as calling it just once. Once again, it worked 
because our function was IO bound. The same thing did not work above when the function was CPU bound.  
  
## There is still hope with CPU bound tasks!  

Turns out there is `multiprocessing.Process` class in Python which offers similar functionality and interface to the `Thread` class. The difference is 
that it uses sub-processes instead of threads. That's why, it won't be blocked by the GIL. Awesome! Let's try that out with the above examples. 
As I said, it offers a similar interface to the `Thread` class and thus we will just have to replace `Thread` with `Process` and we are done:

```python
from multiprocessing import Process
from time import time

before = time()

process1 = Process(target=count_down, args=(100000000,))
process2 = Process(target=count_down, args=(100000000,))

process1.start()
process2.start()

process1.join()
process2.join()

after = time()
print(after-before)
```

It took ~8 seconds on my machine. That is as much as it took when we called the function just once. Cool! Try adding one more process and it will still take 
the same time. That is awesome! However, do keep in mind that processes run in a separate memory space thus can't share data with each other, whereas, 
threads can.

Also keep in mind that we are talking about the CPython here. Other implementations such Jython and IronPython don't have GIL so they can use `Thread`s.
If you don't know what Jython or IronPython are, refer to this [post of mine](/posts/what-is-python/).

Thanks for reading and make sure to leave a comment if you have any questions.

Fight on!
