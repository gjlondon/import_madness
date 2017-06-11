__author__ = 'rogueleaderr'
import random
import time


def merge_sort(input_list):
    if len(input_list) < 2:  # it's a leaf
        return input_list
    else:
        # split
        split_point = len(input_list) // 2
        left_portion, right_portion = input_list[:split_point], input_list[split_point:]

        # recursion
        left_sorted = merge_sort(left_portion)
        right_sorted = merge_sort(right_portion)

        # merge
        merged_list = []
        while left_sorted or right_sorted:
            if not left_sorted:
                bigger = right_sorted.pop()
            elif not right_sorted:
                bigger = left_sorted.pop()
            elif left_sorted[-1] >= right_sorted[-1]:
                bigger = left_sorted.pop()
            else:
                bigger = right_sorted.pop()
            merged_list.append(bigger)
        merged_list.reverse()
        return merged_list


# get the source code from docstring
merge_sort_algo = __doc__

# make a random list
list_to_sort = [int(1000 * random.random()) for i in range(100)]

# write the algorithm into a module
with open("merge_sort.py", "w") as f:
    adjusted_source = merge_sort_algo.replace('input_list = []',
                                              'input_list = {}'.format(list_to_sort))
    f.write(adjusted_source)


import sys
import inspect
import os
import importlib

left_portion = []
import re

while True:


    # get the source code
    current_module = sys.modules[__name__]
    module_source = inspect.getsource(current_module)

    # "pass an argument" by writing our sublist into the source code
    new_list_slug = 'input_list = ' + str(left_portion)
    adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)

    # write the modified code to a new module
    left_path = "left.py"
    with open(left_path, "w") as f:
        f.write(adjusted_source)

    # clear out caches
    importlib.invalidate_caches()
    if "left" in sys.modules:
        del sys.modules['left']

    # execute!
    from left import sorted_sublist as left_sorted

    # clean up
    if os.path.isfile(left_path):
        os.remove(left_path)


# buckle up!
from merge_sort import sorted_sublist as sorted_list






left_sorted





"""
# This is the algorithm we'll use:

import sys
import re
import inspect
import os
import importlib
import time

input_list = []
sublist = input_list
is_leaf = len(sublist) < 2
if is_leaf:
    sorted_sublist = sublist
else:
    split_point = len(sublist) // 2
    left_portion = sublist[:split_point]
    right_portion = sublist[split_point:]

    current_module = sys.modules[__name__]
    module_source = inspect.getsource(current_module)

    left_path = "left.py"
    with open(left_path, "w") as f:
        new_list_slug = 'input_list = ' + str(left_portion)
        adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
        f.write(adjusted_source)

    importlib.invalidate_caches()

    if "left" in sys.modules:
        del sys.modules['left']

    from left import sorted_sublist as left_sorted
    if os.path.isfile(left_path):
        os.remove(left_path)

    right_path = "right.py"
    with open(right_path, "w") as f:
        new_list_slug = 'input_list = ' + str(right_portion)
        adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
        f.write(adjusted_source)

    importlib.invalidate_caches()

    if "right" in sys.modules:
       del sys.modules['right']
    from right import sorted_sublist as right_sorted

    if os.path.isfile(right_path):
        os.remove(right_path)

    # merge
    # TODO use a better merge
    merged_list = []
    while (left_sorted or right_sorted):
        if not left_sorted:
            bigger = right_sorted.pop()
        elif not right_sorted:
            bigger = left_sorted.pop()
        elif left_sorted[-1] >= right_sorted[-1]:
            bigger = left_sorted.pop()
        else:
            bigger = right_sorted.pop()
        merged_list.append(bigger)
    merged_list.reverse()
    sorted_sublist = merged_list

sys.modules[__name__].sorted_sublist = sorted_sublist


"""

import random
import os
import time

random.seed(1001)

list_to_sort = [int(1000*random.random()) for i in range(100)]
print("unsorted: {}".format(list_to_sort))

mergesort = __doc__
with open("merge_sort.py", "w") as f:
    adjusted_source = mergesort.replace('input_list = []', 'input_list = {}'.format(list_to_sort))
    f.write(adjusted_source)

from merge_sort import sorted_sublist as sorted_list

os.remove("merge_sort.py")
finished_time = time.time()

print("original sorted: {}".format(sorted(list_to_sort)))
print("import sorted: {}".format(sorted_list))

assert sorted_list == sorted(list_to_sort)


