from time import time


def count_down(n):
    while n > 0:
        n -= 1

before = time()
count_down(100000000)
count_down(100000000)
count_down(100000000)
after = time()

print(after-before)