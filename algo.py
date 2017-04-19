
import sys
import re
import inspect
import os
import importlib

def merge(a, b):
    if len(a) == 0:
        return b
    elif len(b) == 0:
        return a
    elif a[0] < b[0]:
        return [a[0]] + merge(a[1:], b)
    else:
        return [b[0]] + merge(a, b[1:])

input_list = [956, 373, 26, 180, 875, 891, 601, 945, 351, 395, 567, 585, 676, 632, 255, 956, 811, 699, 355, 750, 947, 280, 81, 58, 13, 702, 400, 639, 263, 579, 818, 632, 692, 315, 658, 870, 289, 282, 561, 363, 342, 128, 670, 929, 247, 583, 643, 256, 350, 352, 903, 252, 962, 766, 412, 735, 928, 668, 314, 331, 762, 225, 548, 563, 929, 775, 312, 960, 233, 626, 808, 468, 257, 965, 955, 830, 231, 33, 437, 856, 250, 160, 285, 485, 755, 666, 716, 391, 739, 904, 828, 792, 564, 646, 134, 307, 636, 931, 958, 914]
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

    sorted_sublist = merge(left_sorted, right_sorted)
    sys.modules[__name__].sorted_sublist = sorted_sublist
