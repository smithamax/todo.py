todo.py
=======

An easy to use todo file manager

Still needs a little work but mostly functional


Installation
------------

fairly standard.

```
$ git clone https://Smithamax@github.com/Smithamax/todo.py.git todo
$ cd todo
$ chmod 755 todo.py

```
then

`$ ln -s $PWD/todo.py ~/bin/todo`

or

`$ echo 'alias todo='$PWD'/todo.py' >> ~/.bash_profile`

and restart terminal.


Usage
-----

usage: `todo [-h] [-g | -l] [<command>] [<args> [<args> ...]]`

using the `-l` flag will force the creation of a TODO in the current working directory
using the `-g` flag will force the use of your global TODO file
you should edit the source to set your global file (currently set to `/Users/dom/todo.txt`)

if these flags are omitted todo.py will look in the current directory then fall back to the global todo file

###Commands###

**add, a**

add a task to TODO file
if no argument is passed enters add mode

**list, ls**

list tasks

**do**

mark task as done

**archive**

move tasks marked as done to DONE file

###The TODO File##

TODO files are simple text files, each line is a task
indented lines are sub tasks (limited support so far)

`todo` prepends a `- ` to each task for niceness but this is not required.

done tasks are perpended with `X `, this replaces `- `.


Configuration
-------------

By default todo.py works without a config file.
However if you wish to set a custom the behavior there are a few options.

example ~/.todoconfig

```
[global]
filename: TODO
dir: ~/
donefilename: DONE

[local]
filename: TODO
donefilename: DONE

```

you can also give a directory its own local settings

/some/directory/.todo

```
[local]
filename: TODO
donefilename: DONE

```

you will still need to force the initial creation of the local file with `todo -l`


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

