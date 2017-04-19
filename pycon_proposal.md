##TITLE

import madness  # how to implement mergesort using only import statements

##CATEGORY

Bad Ideas

##DURATION

I prefer a 30 minute slot

##DESCRIPTION

Recently I had trouble importing a module. So I started actually reading the documentation about the Python import
system and realized that I had been writing Python for years without understanding basics like "a module is a file"
or "importing a module executes it".

A few days later I had a terrible realization -- it's possible to implement the merge sort algorithm in Python using
only the `import` statement.

This talk will walk through my (working!) implementation ([which can be found here](https://github.com/rogueleaderr/import_madness/blob/master/mergesort.py)) and use it as a teaching tool to 1) illustrate what actually
happens when you `import` and 2) spark some creative thinking about how Python's dynamism allows for truly
 inadvisable metaprogramming.

##AUDIENCE

* Any Python developer who has ever downloaded and `import`ed code without reading it first.
* People who enjoy watching intellectual train wrecks.
* Intermediate developers who are starting to get curious about how the Python language actually works.

##PYTHON LEVEL

Novice / Intermediate

##OBJECTIVES

Attendees will leave with:

* A solid conceptual (if high level) understanding of the key pieces of the python import system, including modules, `importlib`, `__import__()`, `exec`, `sys.modules` and the module cache
* A reminder that python modules have runtime access to their own documentation and source code
* A lesson about the risks of importing untrusted code
* A sore throat from groaning too much at all the terrible things I'm doing with our beautiful language
* Hopefully a bit of inspiration to think of creative ways that Python's dynamic interpreted nature can be used to unlock functionality that is not even possible in most other programming languages

##DETAILED ABSTRACT

Just about everyone who has ever used python has used the `import` keyword. Like any good tool, `import` does its job reliably and quietly. I programmed professionally for years without giving more than a few moments thought to what was actually happening when I wrote `import`. The only time I did pay attention was when `ImportError` made an unwelcome appearance.

And then I upgraded some code to Python 3 and imports stopped working, because I had been misusing relative imports in a way that Python 2 allowed and 3 evidently did not. So I sat down and actually read the documentation. And that's the first time that I actually appreciated how much is happening under the hood.

And then, because there is something wrong with me, I got the urge to do something dastardly with these newfound powers. The first idea that came to mind was to implement a recursive sorting algorithm using nothing but the `import` keyword.

I wasn't sure it would be possible up until the point that I actually got it to work. But now I have it written and it does work [and you can see it here](https://github.com/rogueleaderr/import_madness/blob/master/mergesort.py). 

Here's how it works, in a nutshell: create a Python source file and give it a docstring that contains an implementation of mergesort written as a comment. At runtime, read in the module's docstring. Now generate a random list of numbers and interpolate it into the docstring using a regex replacement. Now write out a new file containing the mergesort source code. Then import that source code. Because the merge sort is a recursive algorithm, if itself will need to construct and import new source files for each recursive step. (Make sure to delete the newly created source files once they've been imported to avoid name conflicts and to avoid leaving behind a mess of files.)

I think my demented little program (<100 lines of code) has substantial instructional value. Understanding it requires diving pretty deeply into the import and module system and provides a pretty stark example of just how much radical freedom an interpreted dynamic language offers to the programmer. And because the example is bizarre, I think that walking through it would be entertaining enough to capture people's attention and keep them engaged while they learn about what might otherwise be a fairly dry topic.

In this talk, I intend to start out by showing a prerecorded video screencast of me creating a random list in the Python interpreter and then sorting that list just by importing `sorted_list` from my `mergesort` module. Then I will take a step back and walk through a (simplified) flowchart and perhaps a few slides that explain at a high-level how the Python import system works and what actually happens when you import a module (i.e. Python creates a code object, `exec`'s it, and binds the results into the calling namespace).

Then I will walk step by step through my code (probably broken down into key chunks shown on slides) and use each step to illustrate a key concept:

  1) Python code is interpreted. And the programmer is free to redirect the interpreter at runtime.
 
  2) Importing a module means directing the interpreter's attention into another file (which is why it's valid if inadvisable to place an import statement inside of a function definition).
 
  3) The code that you import get executed, and `def` statements just bind a function to a name (which is also why you can nest function definitions inside of other function definitions).
 
  4) If there is malicious code buried in a file you import, that code can be executed without you ever realizing.
 
  5) Python modules have access to their own doc strings and source code at run time
 
  6) Running Python programs can generate *and run* new Python source code
 
  7) Name spaces (which are honking a great idea) are attached to modules, work like dictionaries, and help us keep our variables organized and avoid name conflicts.
 
  8) Modules live inside sys.modules and are cached to avoid unnecessary repeated execution.
 
  9) But we can clear the cache if we actually do want repeated execution or if we want to import a different module with the same name.
 
  10) Running Python programs can delete their own source code and keep running!
 
  11) You *can* do Lisp-style metaprogramming in Python. You probably shouldn't, but you can.

PyCon has seen several excellent talks about the import system in recent years (including Brett Cannon in 2013 and Allison Kaptur in 2014) and I'm indebted to their ideas for my inspiration. I hope this entertaining example can continue that tradition and help deepen the community's understanding and interest in our powerful import system. And I hope that I can open some eyes and inspire some Python programmers to think about language dynamism in a new way and maybe even come up with some actual good reasons to do bad things with Python.

##OUTLINE

### Live "pressing play on a prerecorded screencast" (2 min)

* Opening a vanilla Python interpreter

* Generating a random list of numbers

* Running `from madness import sorted_list`

* Showing that sorted_list now contains our random list of numbers, sorted

* Pausing for gasps of amazement

### High-level overview of the python import system (10 minutes)
* `import` is syntactic sugar for __import__()

* Modules are discovered using pathfinders and sys.path

* Modules are turned into code objects and `exec`'d

* sys.modules keeps track of everything that's been imported

* Names are bound in the importer's namespace

### A walk through my merge sort code (7 minutes)
* The actual algorithm code is stored as a doc string on the top level module

* we insert our random list into a predefined place in the doc_string using regex replacement

* we interpolate our list-to-be-sorted into the docstring and write the result to a new file

* we import the new file and repeat recursively, spliting the list down to invididual elements

* we unwind our stack, merging together the sorted subcomponents

* we delete our temporary source code files to avoid leaving a mess

* we bind our sorted list into the parent namespace

### Meditations on the power of interpreted dynamism (6 minutes)
* A brief comparison with static, linked languages like C

* a brief discussion of what we gain from static analysis during compilation versus what we lose in being able to modify program behavior at run time

* a brief discussion of the Church-Turing thesis and the idea that computation is a process that can be executed by many substrates and there is no one right path to the top of the mountain

* (if I can find some) a few examples of non-insane runtime code generation, e.g. the `@attrs` library or `macropy`

* an example of how merely importing a library off Github without reading it it can silently upload all of your ssh keys onto pastebin

### Time for questions (5 minutes)


##ADDITIONAL NOTES

I have presented at a non-Python meetup once before. It went well! I'm excited speak on a bigger stage and unleash some `import madness` into the world.

I intend to release all of the code from the project (not that it actually requires much code) on Github and write an accompanying blog post that walks through all of the subject matter in more detail. I will also pitch the talk at the local San Francisco Python meetup to try to get some practice.

This talk uses features that I'm pretty sure are specific to Python 3 and delves into the specifics of Python 3's rewritten `importlib`. So maybe it'll help show people why Python 3 is great. 

Once I flesh out the talk, if it's too long I can cut back on the closing meditations. If it's too short, I can add to the meditations, or talk more about metaprogramming in other languages, or talk about the import system in greater depth.

##ADDITIONAL REQUIREMENTS

It would be really cool if we could put a robotic actuator on the light switch so that I could turn off the room lights using an `import` statement.
