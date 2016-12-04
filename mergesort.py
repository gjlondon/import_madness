# We use the following merge sort algorithm:
from importlib._bootstrap_external import PathFinder

import inspect
import random
import re
import sys
import os

list_to_sort = [47, 77, 22, 55, 78, 3, 37, 36, 96, 54, 12, 95, 100, 82, 83, 6, 96, 63, 28, 14, 58, 98, 51, 91, 13,
                58, 89, 79, 62, 24, 32, 9, 63, 87, 89, 3, 73, 93, 44, 69, 17, 57, 7, 69, 84, 11, 32, 90, 7, 22, 74,
                33, 4, 18, 2, 57, 77, 2, 6, 88, 75, 44, 71, 36, 100, 77, 64, 65, 5, 34, 88, 34, 24, 16, 1, 23, 86,
                12, 52, 7, 96, 10, 1, 91, 41, 92, 98, 68, 41, 50, 7, 70, 99, 87, 67, 79, 80, 47, 90, 47]

list_to_sort = [int(1000*random.random()) for i in range(100)]


def merge(a, b):
    if len(a) == 0:
        return b
    elif len(b) == 0:
        return a
    elif a[0] < b[0]:
        return [a[0]] + merge(a[1:], b)
    else:
        return [b[0]] + merge(a, b[1:])


mergesort = """
import sys
import re
import inspect
import os
import importlib
#from importlib._bootstrap_external import PathFinder

def merge(a, b):
    #ret = a + b
    #print("merging: " + str(a) + " : " + str(b) + "into " + str(ret))

    #return ret
    if len(a) == 0:
        return b
    elif len(b) == 0:
        return a
    elif a[0] < b[0]:
        return [a[0]] + merge(a[1:], b)
    else:
        return [b[0]] + merge(a, b[1:])

input_list = []
sublist = input_list
#print(sublist)
sorted_sublist = "mancy"
#import ipdb ; ipdb.set_trace()
if len(sublist) < 2:
    #print('bottom' + str(sublist))
    sorted_sublist = sublist
else:

    #print("sublist length: " + str(len(sublist)))
    split_point = len(sublist) // 2
    left_portion = sublist[:split_point]
    right_portion = sublist[split_point:]
    current_module = sys.modules[__name__]

    #for side in ("left", "right"):
    #    if side in sys.modules:
    #        del sys.modules[side]
    module_source = inspect.getsource(current_module)

    
    left_path = "steps/left.py"
    with open(left_path, "w") as f:
        new_list_slug = 'input_list = ' + str(left_portion)
        #print(new_list_slug)
        adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
        f.write(adjusted_source)

    # neccesary to find dynamic module
    steps_dir = os.path.join(os.getcwd(), "steps")
    if steps_dir not in sys.path:
        sys.path.insert(0, steps_dir)
    #path_finder = next(finder for finder in sys.meta_path if finder is PathFinder)
    #path_finder.invalidate_caches()
    importlib.invalidate_caches()
    if "steps.left" in sys.modules:
        del sys.modules['steps.left']
    try:
        #print("left")
        from .left import sorted_sublist as left_sorted

    except ImportError as e:
        print(e)
        import ipdb; ipdb.set_trace()
        #print(sys.modules.keys())
        print(sys.meta_path)
        pf = sys.meta_path
        #print(os.getcwd())
        print(__loader__)
        print(__spec__)
        raise e


    #if "steps.left" in sys.modules:
    #    del sys.modules['steps.left']

    #if os.path.isfile(left_path):
    #    os.remove(left_path)
        
    right_path = "steps/right.py"
    with open(right_path, "w") as f:
        new_list_slug = 'input_list = ' + str(right_portion)
        adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
        f.write(adjusted_source)

    #path_finder.invalidate_caches()
    importlib.invalidate_caches()
    #print("right")

    if "steps.right" in sys.modules:
        del sys.modules['steps.right']
    from .right import sorted_sublist as right_sorted
    #if "steps.right" in sys.modules:
    #    del sys.modules['steps.right']
    #if os.path.isfile(right_path):
    #    os.remove(right_path)
    #print("left: " +str(left_sorted))
    #print("right: " +str(right_sorted))
    #import ipdb ; ipdb.set_trace()
    #print(__name__)

    sorted_sublist = merge(left_sorted, right_sorted)
    sys.modules[__name__].sorted_sublist = sorted_sublist

"""
del sys.meta_path[1]
# del sys.modules[__name__]
with open("steps/algo.py", "w") as f:
    adjusted_source = mergesort.replace('input_list = []', 'input_list = ' + str(list_to_sort))
    f.write(adjusted_source)

from steps.algo import sorted_sublist as sorted_list

os.remove("steps/algo.py")
print("sorted: " + str(sorted_list))
my_list = "ank"
# print(sorted_list)
