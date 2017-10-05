


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
print("\n\n\n\n\n\n\nRandom List to Sort: {}".format(list_to_sort))
input("\nContinue? ")

start_time = time.time()
mergesort = __doc__

print("\n\nMerge sort code read from docstring...")
input("\nContinue? ")

with open("merge_sort.py", "w") as f:
    adjusted_source = mergesort.replace('input_list = []', 'input_list = {}'.format(list_to_sort))
    f.write(adjusted_source)

print("\n\nList interpolated into source code. Merge sort code written to merge_sort.py...")
input("\nContinue? ")

from merge_sort import sorted_sublist as sorted_list

os.remove("merge_sort.py")
finished_time = time.time()

print("\n\nList sorted using import system: {}".format(sorted_list))
print("\nSort took {}ms".format(finished_time - start_time))

print("\n\nVerifying sorting against conventional sorted()")
assert sorted_list == sorted(list_to_sort)

input("\nContinue? ")
print("\n\nImport sort succeeded!\n\n\n")

input("\nExit? ")

