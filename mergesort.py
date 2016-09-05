
# We use the following merge sort algorithm:

import inspect
import re
import sys
import os

list_to_sort = [47, 77, 22, 55, 78, 3, 37, 36, 96, 54, 12, 95, 100, 82, 83, 6, 96, 63, 28, 14, 58, 98, 51, 91, 13, 58, 89, 79, 62, 24, 32, 9, 63, 87, 89, 3, 73, 93, 44, 69, 17, 57, 7, 69, 84, 11, 32, 90, 7, 22, 74, 33, 4, 18, 2, 57, 77, 2, 6, 88, 75, 44, 71, 36, 100, 77, 64, 65, 5, 34, 88, 34, 24, 16, 1, 23, 86, 12, 52, 7, 96, 10, 1, 91, 41, 92, 98, 68, 41, 50, 7, 70, 99, 87, 67, 79, 80, 47, 90, 47]

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

input_list = []
sublist = input_list
print(sublist)
sorted_sublist = []
if len(sublist) < 2:
    sorted_sublist = sublist
else:

    print("sublist length: " + str(len(sublist)))
    split_point = len(sublist) // 2
    left_portion = sublist[:split_point]
    right_portion = sublist[split_point:]
    current_module = sys.modules[__name__]

    #for side in ("left", "right"):
    #    if side in sys.modules:
    #        del sys.modules[side]
    module_source = inspect.getsource(current_module)
    print(os.getcwd())

    with open("steps/left.py", "w") as f:
        new_list_slug = 'input_list = ' + str(left_portion)
        adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
        f.write(adjusted_source)

    #del sys.modules["left"]
    # neccesary to find dynamic module
    steps_dir = os.path.join(os.getcwd(), "steps")
    sys.path.insert(0, steps_dir)
    try:
        from .left import sorted_sublist
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

    left_path = "steps/left.py"
    if os.isfile(left_path):
        os.remove(left_path)
    except FileNotFoundError:
        import glob
        from os.path import dirname, basename, isfile
        files = glob.glob(dirname(__file__)+"/*.py")
        print(files)
"""

#del sys.modules[__name__]
with open("steps/algo.py", "w") as f:
    adjusted_source = mergesort.replace('input_list = []', 'input_list = ' + str(list_to_sort))
    f.write(adjusted_source)
from steps.algo import sorted_sublist as sorted_list
os.remove("steps/algo.py")
print(sorted_list)
my_list = "ank"
#print(sorted_list)
