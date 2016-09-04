__author__ = 'rogueleaderr'
# basic merge sort implementation from http://stackoverflow.com/a/4574358/998687
import random

"""
import inspect
"""
def merge(a, b):
    if len(a) == 0:
        return b
    elif len(b) == 0:
        return a
    elif a[0] < b[0]:
        return [a[0]] + merge(a[1:], b)
    else:
        return [b[0]] + merge(a, b[1:])

def mergesort(x):
    if len(x) < 2:
        return x
    else:
        h = len(x) // 2
        return merge(mergesort(x[:h]), mergesort(x[h:]))

if __name__ == "__main__":
    print("let's get startedswitch to command mode")
    to_sort = [random.randint(0, 100) for i in range(0, 100)]
    print(mergesort(to_sort))
