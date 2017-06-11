import time

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
