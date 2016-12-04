import random
import os

list_to_sort = [int(1000*random.random()) for i in range(100)]

mergesort = """
import sys
import re
import inspect
import os
import importlib

input_list = []
sublist = input_list
if len(sublist) < 2:
    # leaf
    sorted_sublist = sublist
else:
    split_point = len(sublist) // 2
    left_portion = sublist[:split_point]
    right_portion = sublist[split_point:]
    current_module = sys.modules[__name__]
    module_source = inspect.getsource(current_module)

    # neccesary to find dynamic module
    steps_dir = os.path.join(os.getcwd(), "steps")
    if steps_dir not in sys.path:
        sys.path.insert(0, steps_dir)

    left_path = "steps/left.py"
    with open(left_path, "w") as f:
        new_list_slug = 'input_list = ' + str(left_portion)
        adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
        f.write(adjusted_source)

    importlib.invalidate_caches()

    if "steps.left" in sys.modules:
        del sys.modules['steps.left']
    from .left import sorted_sublist as left_sorted
    if os.path.isfile(left_path):
        os.remove(left_path)
        
    right_path = "steps/right.py"
    with open(right_path, "w") as f:
        new_list_slug = 'input_list = ' + str(right_portion)
        adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
        f.write(adjusted_source)

    importlib.invalidate_caches()

    if "steps.right" in sys.modules:
        del sys.modules['steps.right']
    from .right import sorted_sublist as right_sorted
    if os.path.isfile(right_path):
        os.remove(right_path)

    # merge
    sorted_sublist = []
    while (left_sorted or right_sorted):
        if not left_sorted:
            bigger = right_sorted.pop()
        elif not right_sorted:
            bigger = left_sorted.pop()
        elif left_sorted[-1] > right_sorted[-1]:
            bigger = left_sorted.pop()
        else:
            bigger = right_sorted.pop()
        sorted_sublist.append(bigger)
    sorted_sublist.reverse()

    sys.modules[__name__].sorted_sublist = sorted_sublist
"""

with open("steps/algo.py", "w") as f:
    adjusted_source = mergesort.replace('input_list = []', 'input_list = {}'.format(list_to_sort))
    f.write(adjusted_source)

from steps.algo import sorted_sublist as sorted_list

os.remove("steps/algo.py")
print("sorted: " + str(sorted_list))
