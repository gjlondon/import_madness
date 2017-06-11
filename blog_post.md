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

This post is about how an ImportError lead me to a strange place. 

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

 
 