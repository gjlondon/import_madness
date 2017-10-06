import time
import random

__author__ = 'rogueleaderr'


def bubble_sort(list_to_sort):
    start_time = time.time()

    while True:
        list_len = len(list_to_sort)
        max_index = (list_len - 1)
        swaps = 0
        for i in range(list_len):
            j = i + 1
            if j > max_index:
                break
            if list_to_sort[i] > list_to_sort[j]:
                list_to_sort[j], list_to_sort[i] = list_to_sort[i], list_to_sort[j]
                swaps += 1
        if swaps == 0:
            break

    finished_time = time.time()
    print("Sort took {}".format(finished_time - start_time))
    return list_to_sort


if __name__ == "__main__":
    # for t in (100, 1000, 10000, 100000):
    for t in (5000, 6500, 7500, 8500, 10000, 15000, 20000, 25000):
        list_to_sort = [int(1000 * random.random()) for i in range(t)]
        print(t)
        bubble_sort(list_to_sort)