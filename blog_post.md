>>Sing, goddess, the rage of George and the ImportError,
>>
>>and its devastation, which put pains thousandfold upon his programs,
>>
>>hurled in their multitudes to the house of Hades strong ideas
>>
>>of websites, but gave their code to be the delicate feasting
>>
>>of dogs, of all birds, and the will of Guido was accomplished
>>
>>since that time when first there stood in division of conflict
>>
>>Brett Cannon’s son the lord of modules and brilliant `import` keyword. . . .

# Backstory

This post is about how an `ImportError` lead me to a very strange place. 

I was sitting alone at home, writing a simple Python program. It was one of my first attempts at Python 3.
 
I tried to import some code and got an `ImportError`. Normally I solve `ImportError`'s by shuffling files around until 
they go away. But this being Python 3, none of my shuffling solved the problem. So I found myself actually reading the
official documentation for the Python import system. Somehow I'd spent over five years writing Python code professionally
without ever actually reading that particular bit of documentation.

Well -- what I learned there changed me.

First of all, I answered by simple question, which is when to use `.`'s in an import: 
 
    from .spam import eggs  # when spam.py is in the same directory (i.e. "package" as the code doing the import)
    from ..spam import eggs  # when spam.py is in the *enclosing* package, i.e. one level up
    import .spam  # ImportError! At least in Python 3, you can only use the dots with the `from a import b` syntax
      
But second and more importantly, I realized that this whole time I had never really understood what the word **module**
means in Python.

According to the official documentation, a "module" is [a file containing Python definitions and statements](https://docs.python.org/3/tutorial/modules.html).

In other words, `spam.py` is a module.

But it's not quite that simple. In my running Python program, if I `import requests`, then what is `type(requests)`?

It's `module`.
 
That means module is a type of object in a running Python program. And `requests` in my running program is *derived* 
from requests.py, but it's not the same thing.

So what is the `module` *class* in Python and how is a babby module formed?
 
Modules are created automatically in Python when you import. It turns out that the `import` keyword in Python is 
syntactic sugar for a somewhat more complicated process. When you `import requests`, Python actually does two things:
 
1) Calls an internal function: `__import__('requests')` to create the `requests` module object
2) Binds the local variable `requests` to that module

And then does `__import__()` do?

Well, it's complicated. I'm not going to go into full detail, but [there's a great video](http://pyvideo.org/pycon-us-2013/how-import-works.html) where Brett Cannon, the main
maintainer of the Python import system painstakingly walks through the whole shebang.

But in a nutshell, importing in Python has 5 steps:

### See if the module has already been imported  

Python maintains a cache of modules that have already been imported. The cache is a dictionary held at `sys.modules`.

If you try to import `requests`, `__import__` will first check if there's a module in `sys.modules` named `requests`. If there is,
Python just gives that module right back and not do any more work.

If the module isn't cached (usually because it hasn't been import yet, but almost maybe because someone did some nefarious... then:

### Find the source code using sys.path

`sys.path` is a list in every running Python program that tells the interpreter where it should look for modules when 
it's asked to import them. Here's an excerpt from my current sys.path:

    '',  # the directory our code is running in 
    '/Users/rogueleaderr/miniconda3/lib/python3.5',  # where my Python executable lives  
    '/Users/rogueleaderr/miniconda3/lib/python3.5/site-packages'  # the place where `pip install` puts stuff
    
When I `import requests` Python goes and looks in those directories for `requests.py`. If it can't find it, I'm in for an
`ImportError`. I'd estimate that the large majority of real life `ImportError`'s happen because the source code you're 
trying to import isn't in a directory that's on `sys.path`. Move your module or add the directory to `sys.path` and you'll have a better day.

In Python 3, you can do some pretty crazy stuff to tell Python [to look in esoteric places for code](https://docs.python.org/3/reference/import.html#the-meta-path). But that's a topic for another day!

### Make a Module object

Python has a built in type called `ModuleType`. Once `__import__` has found your source code, it'll create 
a new `ModuleType` instance and attach the your `module.py`'s source code to it.

Then, the exciting part:

### Executes the module source code!

`__import__` will create a new *namespace*, i.e. scope, i.e. the `__dict__` attribute attached to most Python objects. 
And then it will actually `exec` your code inside of that namespace.

Any variables or functions that get defined during that execution around captured in that namespace. And the namespace is
attached to the newly created module, which is itself then returned into to the importing scope.
 
### Cache the module inside `sys.modules` 

If we try to `import requests` again, we'll get the same module object back. Steps 2-5 will not be repeated.

Okay! This is a pretty cool system. It let's us write many pretty Python programs.

But, if we're feeling demented, it also lets us write some **pretty dang awful** Python programs.
 
# Where it gets weird

So what I learned helped me fix my immediate import problem. But that wasn't enough.
 
![Gizmo gets wet](https://cdn.drawception.com/images/panels/2012/5-21/RmX2j1QgFn-2.png)

With these new import powers in hand, I immediately starting thinking about how I could use them for evil, 
rather than good. Because, as we know:
 
![Good is dumb](https://cdn.shopify.com/s/files/1/1119/4994/products/0_6402f71a-5840-4e65-903c-01c4dd32fc13_1024x1024.jpg?v=1478168644)
(c. Five Finger Tees)

So far, the worst idea I've had for how to misuse the Python import system is to 
**implement a mergesort algorithm using just the import keyword**. At first I didn't know if it was possible. But, *spoiler alert* it is!

It took me a fair amount of time to do because you have to subvert a lot of very well-intentioned, normally helpful machinery in the import system.
 
But we can do it, and here's how:

Remember that when we import a module, Python executes all the source code.

So imagine I start up Python and define a function:
     
    >>> def say_beep():
    >>>    print("beep!.........beep!")
    >>>    return "beep"
        
    >>> say_beep()
    
This will print out some beeps.

Now imagine instead I write the same 4 lines of code as above into a file called `say_beep.py`. Then I open my 
interpreter and run

    >>> import say_beep.py
    
What happens? **The exact same thing**...Python prints out some beeps.

If I create a module that contains the same source code as the body of a function, then importing the module 
will produce the same result as calling the function.

Well, what about `return`? Simple:

    # make_beeper.py
    
    beeper = lambda x: print("say beep")

    # main.py
    
    from make_beeper import beeper
    beeper()
    
Anything that gets defined in the module is available in the module's namespace after it's imported. So `from a import b`
is structurally the same as `b = f()`

Okay, what about passing arguments? Well, that gets a bit harder. The trick is that we source code is just text, so we 
can modify the source of a module before we import it:
 
    # with_args.py
    
    a = None
    b = None
    result = a + b

    # main.py
    
    src = ""
    with open("with_args.py") as f:
        for line in f:
        src += line
        
    a = 10
    b = 21
    
    src = src.replace("a = None", a)
    src = src.replace("b = None", b)
    
    with open("with_args.py", "w") as f:
        for line in src.split("\n"):
            f.write(line)
            
    from with_args import result
    print(result)  # it's 31!
    
Now this certainly isn't pretty. But where we're going, nothing is pretty. Buckle up!

## How to mergesort

Okay..how can we apply these ideas to implement mergesort?

First, let's quickly review what mergesort is: it's a recursive sorting algorithm with *n log n* worst-case computational complexity
(meaning it's pretty darn good, especially compared to bad sorting algorithms like bubble sort that have *n^2* complexity.)

It works by taking a list, splitting it in half, and then splitting the halves in half until we're left with individual elements.

Then we *merge* adjacent elements by interleaving them in sorted order. Take a look at this diagram:

![picture of mergesort](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Merge_sort_algorithm_diagram.svg/450px-Merge_sort_algorithm_diagram.svg.png)
 
Or read [the Wikipedia article](https://en.wikipedia.org/wiki/Merge_sort) for more details.

## Some rules

1. No built in sorting functionality. Python's built in `sort` uses a [derivative of merge sort](https://en.wikipedia.org/wiki/Timsort)
so just putting `result = sorted(lst)` into a module and importing it isn't very sporting.
2. No user-defined functions at all.
3. All the source code has to live inside one module file, which we will fittingly call `madness.py`

## The code

Well, here's the code: (Walk-through below, if you don't feel like reading 100 lines of bizarre Python)

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
    
        # get a reference to the code we're currently running
        current_module = sys.modules[__name__]
        # get it's source code using stdlib's `inspect` library
        module_source = inspect.getsource(current_module)
    
        # "pass an argument" by modifying the module's source
        new_list_slug = 'input_list = ' + str(left_portion)
        adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
        
        # make a new module from the modified source
        left_path = "left.py"
        with open(left_path, "w") as f:
            f.write(adjusted_source)
    
        # invalidate caches
        importlib.invalidate_caches()
        if "left" in sys.modules:
            del sys.modules['left']
    
        # "call" the function to "return" a sorted sublist
        from left import sorted_sublist as left_sorted
        
        # clean up by deleting the new module
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
    
    # make sure that the result is available in the **parent's** namespace after this gets overwritten
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
 
That's all we need.

# Breaking it down

### Madness itself

The body of `madness.py` is compact. All it does is generate a random list of numbers, grab our template 
implementation of merge sort from it's own docstring (how's that for self-documenting code?), jam in our random list,
and kick off the algorithm by running `from merge_sort import sorted_sublist as sorted_list`.
 
### The mergesort implementation

This is the fun part.

So for to help make my code understandable, here is a "normal" implementation of merge_sort as a function:

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

It has three phases:

1. Split the list in half

2. Call `merge_sort recursively until the list is split down to individual elements

3. Merge the sublists we're working on this stage into a single sorted sublist by interleaving the elements in sorted order

But since our rule says that we can't use functions, we need to replace the recursive function calls with `import`.

That means replacing this:
    
    left_sorted = merge_sort(left_portion)
    
With this:

    # get a reference to the code we're currently running
    current_module = sys.modules[__name__]
    # get it's source code using stdlib's `inspect` library
    module_source = inspect.getsource(current_module)

    # "pass an argument" by modifying the module's source
    new_list_slug = 'input_list = ' + str(left_portion)
    adjusted_source = re.sub(r'^input_list = \[.*\]', new_list_slug, module_source, flags=re.MULTILINE)
    
    # make a new module from the modified source
    left_path = "left.py"
    with open(left_path, "w") as f:
        f.write(adjusted_source)

    # invalidate caches
    importlib.invalidate_caches()
    if "left" in sys.modules:
        del sys.modules['left']

    # "call" the function to "return" a sorted sublist
    from left import sorted_sublist as left_sorted
    
    # clean up by deleting the new module
    if os.path.isfile(left_path):
        os.remove(left_path)
        
    # make sure that the result is available in the **parent's** namespace after this gets overwritten
    sys.modules[__name__].sorted_sublist = sorted_sublist
    
And that's really it. We have a few lines to trick Python into actually doing the full import process when we import 
a module with the same name as one that's already been imported. (If our merge sort execution tree has multiple levels, 
we're going to have a lot of different left.py's). 

And that's how you abuse the Python import system to implement mergesort.

# Many paths to the top of the mountain, but the view is a singleton.

It's pretty mindblowing (to me at least) that this approach works at all. But on the other hand, why shouldn't it?

One of the most fundamental ideas in computer science is the [Church-Turing thesis](https://plato.stanford.edu/entries/church-turing/). 
It states that any effectively computable function can be computed by a universal Turing machine. The thesis is usually 
trotted out to explain why there's nothing you can compute with a universal Turing machine that you can't compute using 
lambda calculus, and therefore there's no program you can write in C that you can't, in principle, write in Lisp. But as 
corollary: since you can, if you really want to, implement a Turing tape by writing files to the file system one bit at 
a time and importing the results, you can use the Python import system to simulate a Turing machine. That implies that, 
in principle, any computation that can be performed by a digital computer can be performed (assuming infinite patience) 
using the Python import system.

The Python community spend a lot of time advocating for good methodology and "idiomatic" coding styles, and for good reason!
If you're writing software that's intended to be used, some methods are almost always better than their alternatives.

But if you're writing programs to **learn**, sometimes it's helpful to remember that there are [many different models
of computation under the sun](http://www.ybrikman.com/writing/2014/04/09/six-programming-paradigms-that-will/). And especially in the
era when "deep learning", i.e. [graph-structured computations](http://deeplearning.net/software/theano/extending/graphstructures.html) that simulate differentiable functions, is really starting to shine,
it's extra important to remember that sometimes taking a completely different (and even wildly "inefficient") approach to 
a computational problem can lead to [startling success](https://en.wikipedia.org/wiki/AlphaGo).

It's also nice to remember that Python itself started out as (and in a sense still is!) a ridiculously inefficient 
and roundabout way to execute C code. 

Abstractions really matter. In the [words](https://en.wikiquote.org/wiki/Alfred_North_Whitehead) of Alfred North Whitehead, 

>> Civilization advances by extending the number of important operations which we can perform without thinking about them

My "import sort" is certainly not a useful abstraction. But I hope that learning about it will lead you to some good ones! 
 
## Note Bene

In case it's not obvious, you should never actually do this in any code that you're intending to actually use for anything.
 
But the general idea of modifying Python source code at import time has at least one legitimate 
(if not necessary advisable) use case: **macros**.

Python has a library called [macropy](https://github.com/lihaoyi/macropy) that implements Lisp-style syntactic macros in Python
by modifying your source code at import time.

I've never actually used macropy, but it's pretty cool to know that Python makes the simple things easy and the insane things possible.

Finally, as bad as this mergesort implementation is, it allowed me to run a fun little experiment. We know that 
merge sort has good computation complexity compared to naive sorting algorithms. But how long does a list be before a
standard implementation of bubble sort runs slower than the awful import-based implementation of mergesort? It turns out
that a list only has to be about 50k items long before **"import sort" is faster than bubble sort**.

Computational complexity is a powerful thing!

All the code for this post is [on Github](https://github.com/rogueleaderr/import_madness) 