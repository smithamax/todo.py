todo.py
=======

An easy to use todo file manager

Still needs a little work but mostly functional

Usage
-----

usage: `todo [-h] [-g | -l] [<command>] [<args> [<args> ...]]`

using the `-l` flag will force the creation of a todo.txt in the current working directory
using the `-g` flag will force the use of your global todo file
you should edit the source to set your global file (currently set to `/Users/dom/todo.txt`)

if these flags are omitted todo.py will look in the current directory then fall back to the global todo file

###Commands###

**add, a**

add a task to todo file
if no argument is passed enters add mode

**list, ls**

list tasks

**do**

mark task as done

**archive**

move tasks marked as done to done file


Examples
--------

these assume the you have linked to todo.py in your bin folder as todo

    $ todo add this is a task

    $ todo ls
    1 this is a task

    $ todo do 1
    task 1 marked as done

    $ todo ls
    X this is a task

    $ todo archive

