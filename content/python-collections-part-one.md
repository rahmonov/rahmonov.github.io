Title: Python Collections - Counter
Date: 2017-07-21 20:10
Modified: 2017-07-21 20:10
Category: programming
Tags: python, collections, counter
Slug: python-collections-counter
Authors: Jahongir Rahmonov
Summary: The comprehensive guide to Python's collections module. Part One: Counter

Python has the following general purpose built-in containers: `dict`, `list`, `set`, and `tuple`. However, apart from
them, there are specialized alternative container data types in Python's collections module. In this blog post, we will
take a look at the `Counter` class from this module.

Counter
---------------
A Counter is a child class of `dict` which, as its name suggests, counts hashable objects. Basically, it stores elements as
dictionary keys and their counts as dictionary values:


```python
In [1]: from collections import Counter

In [2]: my_list = ['a', 'b', 'c', 'c', 'a', 'd', 'b', 'e', 'a']

In [3]: print(Counter(my_list))
Counter({'a': 3, 'c': 2, 'b': 2, 'e': 1, 'd': 1})
```
    
As you can see that it is unordered and is basically saying there are 3 of 'a' in `my_list` and etc.
     
Besides initializing from an iterable like we saw in the previous example, a Counter can also be initialized from another mapping:
      
```python
In [4]: print(Counter({'car': 6, 'house': 10}))
Counter({'house': 10, 'car': 6}) 

In [5]: print(Counter(car=6, house=10))
Counter({'house': 10, 'car': 6})

In [6]: print(Counter('sibling'))    # another iterable
Counter({'i': 2, 'l': 1, 'b': 1, 'g': 1, 's': 1, 'n': 1}) 
```
            
As a `Counter` is a child of the `dict` class, it has `dict`'s interface:
 
```python
In [7]: c = Counter(my_list)
 
In [8]: c.items()
Out[8]: dict_items([('e', 1), ('c', 2), ('b', 2), ('a', 3), ('d', 1)]) 

In [9]: c.keys()
Out[9]: dict_keys(['e', 'c', 'b', 'a', 'd'])

In [10]: c.values()
Out[10]: dict_values([1, 2, 2, 3, 1]
```

The only difference is that if you try to access a missing item, a Counter will return zero whereas a dict would raise a `KeyError`:

```python
In [11]: c['t']
Out[11]: 0
```
    
Other than those standard `dict` methods, a Counter has 3 more specific ones.

`most_common(n)` - returns a list of `n` most common elements and their counts in a tuple, ordered from the most common to the least.
If `n` is `None`, then the method will return all of the elements:

```python
In [12]: c = Counter('hallelujah')

In [13]: c.most_common(3)
Out[13]: [('l', 3), ('h', 2), ('a', 2)]

In [14]: c.most_common()
Out[14]: [('l', 3), ('h', 2), ('a', 2), ('j', 1), ('u', 1), ('e', 1)]
```
    
`elements()` - returns an iterator which repeats each element as many times as its count:

```python
In [15]: list(c.elements())
Out[15]: ['l', 'l', 'l', 'j', 'u', 'h', 'h', 'e', 'a', 'a']  
```
    
`subtract(iterable-or-mapping)` - Counts of common elements are subtracted from each other

```python
In [16]: d = Counter('hollar')

In [17]: d
Out[17]: Counter({'a': 1, 'h': 1, 'l': 2, 'o': 1, 'r': 1})

In [18]: c
Out[18]: Counter({'a': 2, 'e': 1, 'h': 2, 'j': 1, 'l': 3, 'u': 1})

In [19]: c.subtract(d)

In [20]: c
Out[20]: Counter({'a': 1, 'e': 1, 'h': 1, 'j': 1, 'l': 1, 'o': -1, 'r': -1, 'u': 1})
```
    
Also, some mathematical operations can be applied to combine `Counter` objects:

Adding(+) two Counters together will perform the following on the elements: `c[x] + d[x]`:
         
```python
In [21]: c = Counter(a=3, b=1)

In [21]: d = Counter(a=1, b=2)

In [22]: c + d
Out[22]: Counter({'a': 4, 'b': 3})
```
    
Subtracting(-) is the same as the `subtract()` method (keeps only positive counts):

```python
In [23]: c - d
Out[23]: Counter({'a': 2})
```
    
Intersaction(&) will keep only the minimum of corresponding counts: `min(c[x], d[x]) `:
     
```python
In [24]: c & d
Out[24]: Counter({'a': 1, 'b': 1})
```
    
Union(|) will keep only the maximum of corresponding counts: `max(c[x], d[x])`:
    
```python
In [25]: c | d
Out[25]: Counter({'a': 3, 'b': 2})
```
    
And finally, there are shortcuts for adding an empty counter and subtracting from an empty counter:
   
```python
In [26]: c = Counter(a=2, b=-4)   

In [27]: +c                     # the same as: c + Counter()
Out[27]: Counter({'a': 2})   

In [28]: -c                     # the same as: Counter() - c
Out[28]: Counter({'b': 4}) 
```
    
Now, with all this theoretical knowledge learned, let's try to apply it to solve a real problem. Let's try to tackle [this problem](https://www.hackerrank.com/challenges/collections-counter/problem)
in HackerRank, shall we? Before proceeding further, try to solve it yourself and then compare your solution with mine. Better yet, comment your solution here to discuss.

Task:

    Raghu is a shoe shop owner. His shop has X number of shoes. 
    He has a list containing the size of each shoe he has in his shop. 
    There are N number of customers who are willing to pay x amount of money only if they get the shoe of their desired size.
    
    Your task is to compute how much money Raghu earned.
    
    Input Format
    
    The first line contains X, the number of shoes. 
    The second line contains the space separated list of all the shoe sizes in the shop.
    The third line contains N, the number of customers. 
    The next N lines contain the space separated values of the shoe size desired by the customer and x, the price of the shoe.
    
    Output Format
    
    Print the amount of money earned by Raghu.
    
My solution:

```python
from collections import Counter

X = int(input())
shoes = [int(val) for val in input().split()]
N = int(input())

shoe_collection = Counter(shoes)
total_money = 0

for i in range(N):
    size, money = [int(val) for val in input().split()]

    if shoe_collection.get(size):
        total_money += money
        shoe_collection[size] -= 1

print(total_money)
```
    
It is pretty easy to understand but if you have any questions make sure to ask in the comments!  
  
Fight on!  