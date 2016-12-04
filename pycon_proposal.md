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

This talk will walk through my (working!) implementation and use it as a teaching tool to 1) illustrate what actually
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
* Of throat sore from groaning too much at all the terrible things I'm doing with our beautiful python language
* Hopefully a bit of inspiration to think of creative ways that Python's dynamic interpreted nature can be used to unlock functionality that is not even possible in most other programming languages

##DETAILED ABSTRACT

Just about everyone who has ever used python has used the import keyword. Like a good tool often does, the import keyword does its job reliably and gets out of the way without drawing attention to itself. I programmed professionally for years without ever giving more than a few moments thought to what was actually happening when I called import. And the only time I paid attention to import was when I was getting a `could not import module` error or when I was trying to break a cyclical reference in my code.

And then and then I upgraded some code to Python 3 my imports stopped working because the semantics of .-based relative imports had changed (which is not to say that I even understood how the old system worked--just that I got it to somehow work 1 time). So I sat down and actually read the documentation import keyword for the first time (solidly 5 years into my professional Python career). And that's the first time that I came to actually understand and appreciate how much is happening under the hood).

And then, because there is something wrong with me, I got the urge to misuse these newfound powers in the most spectacular way I could think of. And the first idea that came to mind was to import a recursive sorting algorithm using nothing but the import keyword.

I was not sure at first that it would be possible--I really wasn't sure right up until the moment that I actually got it to work. But now I have it written and it does work. Here's how: create a Python source file and give it a docstring that contains an implementation of merge sort written as a comment. In your python source, read in the  modules docstring at runtime. Now generate a random list of numbers and interpolate it into the doc string using a regular expression replacement. Now write out a new file containing the merge sort source code. And then import that source code. Because the merge sort is a recursive algorithm, if itself will need to build and traverse the 'merge tree' by dynamically creating and writing out new source files for left and right children nodes and then importing those nodes (making sure to delete parent modules from the start modules and module cash to avoid name conflicts and to avoid leaving behind a mess of files.)

I think the program that I ended up with, while demented, has substantial instructional value because understanding it requires diving pretty deeply into the import and module system and provide a pretty stark example of just how much radical freedom an interpreted dynamic language offers to the programmer. And because the example is so bizarre, I think that walking through it would be entertaining enough to capture people's attention and them engaged while they learn about what might otherwise be a fairly dry topic.

  In this talk, I intend to start out by showing a prerecorded video screen cast of me creating a random list in the python interpreter and then sorting that list just by importing `sorted_list` from my merge sort module. Hopefully that magic trick will capture the audience's attention quickly. Then I will take a step back and walk through a (simplified) flowchart and perhaps a few slides that explain at a high level how the python import system works and what actually happens when you import a module (i.e. Python creates a code object, `exec`'s it, and binds the results into the calling name space).

  Then I will walk step by step through my code (probably broken down into key chunks shown on slides) and use each step to illustrate a key concept:

  1) Python code is interpreted, not compiled, meaning that each line is executed when the interpreter gets to it. And the programmer is free to redirect the interpreter at runtime.
  2) Importing a module just means directing the interpreter's attention into another file (which is why it's valid if inadvisable to place an import statement inside of a function definition).
  3) The code that you import get executed, and `def` statements just bind a function to a name (which is also why you can nest function definitions inside of other function definitions).
  4) If there is malicious code buried in a file the gets imported by file that you import, that code can be executed without you ever realizing.
  5) Python modules have access to their own doc strings and source code at run time
  6) Running python programs can generate *and run* new Python source code
  7) Name spaces (which are honking a great idea) are attached to modules, work like dictionaries, help us keep our variables organized and avoid name conflicts.
  8) Modules live inside sys.modules and are cached to avoid unnecessary repeated execution.
  9) But we can clear the cache if we actually do want repeated execution or if we want to import a different module with the same name
  10) Running Python programs can delete their own source code and keep running!
  11) You *can* do Lisp-style metaprogramming in Python. You probably shouldn't, but you can.

PyCon has seen several excellent talks about the import system in recent years (including Brett Cannon in 2013 and Allison Kaptur in 2014) and I'm indebted to their ideas for my inspiration. I hope this entertaining example can continue that tradition and help deepen the community's understanding an interest in our powerful import system. And I hope that I can open some eyes and inspire some Python programmers to think about language dynamism and a new way and maybe even come up with some actual good reasons to do bad things with Python.

##OUTLINE

### Live "pressing play on a prerecorded screencast" (2 min)
* Opening a vanilla python interpreter
* Generating a random list of numbers
* Running `from madness import sorted_list`
* Showing that sorted_list now contains our random list of numbers, sorted
* Pausing for gasps of amazement
### High-level overview of the python import system ( 7 minutes)
* `import` is syntactic sugar for __import__()
* Modules are discovered using pathfinders and sys.path
* Modules are turned into code objects and `exec`'d
* Names are bound in the parents namespace
### A walk through my merge sort code (10 minutes)
* The actual algorithm code is stored as a doc string on the top level module
* we insert our random list into a predefined place in the doc_string using regex replacement
* we write to be interpolated a string into a new file
* we import the new file and repeat recursively printable list is fully split
* we unwind our stack, merging together the sorted subcomponents
* we delete our temporary source code files to avoid leaving a mess
* we bind our sorted list into the parent namespace
### Meditations on the power of interpreted dynamism (6 minutes)
* A brief comparison with static, linked languages like C
* a brief discussion of what we gain from static analysis during compilation
do versus what we lose in being able to modify program behavior at run time
* a brief discussion of the church-turing thesis and the idea that computation is a process that can be executed by many substrates and there is no 1 right path to the top of a mountain
* (if I can find some), a few examples of non-insane uses a runtime code generation, e.g. the @attrs library
* an example of how merely importing a library off Github without reading it it can silently upload all of your ssh keys onto pastebin
### Time for questions (5 minutes)


##ADDITIONAL NOTES

I have presented at a (non-Python) meetup once but I have never presented at a conference before. I'm excited to break the seal and unleash some import madness into the world.

I intend to release all of the code from the project (not that it actually requires much code) on github and write an accompanying blog post that walks through all of the subject matter in more detail. I will also pitch the talk at the local san francisco meetup to try to get some practice.

##ADDITIONAL REQUIREMENTS

It would be really cool if we could put a robotic actuator on the light switch so that I could turn off the lights using an import statement.
