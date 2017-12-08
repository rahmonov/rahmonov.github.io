from threading import Thread
from time import time


def count_down(n):
    while n > 0:
        n -= 1


before = time()

thread1 = Thread(target=count_down, args=(100000000,))
thread2 = Thread(target=count_down, args=(100000000,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

after = time()
print(after-before)
