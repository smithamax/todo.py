#!/usr/bin/python
import argparse, re, os
import fileinput,sys


def parsetask(line):
	done, line = parsedone( line )

	if re.match(r' *[\-xX ] ', line):
		line = re.sub(r' *[\-xX ] ', "", line)

	return done, line

def parsedone(line):
	done = False

	if re.match(r' *[xX] ', line):
		line = re.sub(r' *[xX] ', "", line)
		done = True

	return done, line

def parsefile(f):
	tasks = []
	linenum = 1
	line = f.readline()

	while line:
		line = line.rstrip()
		if line != "":
			if re.match(r'  [xX \-] ', line):
				task.subtasks.append(Task(line, linenum))
			else:
				task = Task(line, linenum)
				tasks.append(task)
		
		line = f.readline()
		linenum += 1

	return tasks

def parsetasknum(tasknum):
	parts = tasknum.split('.')
	if len(parts) == 2:
		return int(parts[0]), int(parts[1])
	else:
		return int(parts[0]), False

def marklinedone(furl, lineno):
	for line in fileinput.input(furl, inplace=1):
		if fileinput.filelineno() == lineno:
			line = re.sub(r'\A( *)[-xX]? *',r'\1X ', line)
		
		sys.stdout.write(line)



class Task(object):
	"""docstring for Task"""
	def __init__(self, line, lineno):
		self.done, self.task = parsetask(line)
		self.line = lineno

		self.subtasks = []


def add_task(text, furl):
	if os.path.isfile(furl):
		f = open(furl, 'a')
	else:
		f = open(furl, 'w')
	
	f.write('- '+str.join(' ',text)+'\n')
	f.close()

def list_tasks(furl):
	f = open(furl, 'r')
	i = 0
	for t in parsefile(f):
		i += 1
		j = 0
		if t.done:
			mark = 'X'
		else:
			mark = str(i)

		print mark, t.task
		for st in t.subtasks:
			j += 1
			if st.done:
				mark = 'X'
			else:
				mark = str(i)+"."+str(j)
			print "  "+ mark, st.task
		if t.subtasks:
			print ""
	f.close()


def do_task(text, furl):
	f = open(furl, 'r')
	tasklist = parsefile(f)
	f.close()


	for t in text:
		i, j = parsetasknum(t)
		task = tasklist[i-1]
		if j:
			task = task.subtasks[j-1]
		linenum = task.line
		marklinedone(furl, linenum)
		print 'task', t, 'marked as done'


	

		

def main():
	parser = argparse.ArgumentParser(description='Task command line utility')

	group = parser.add_mutually_exclusive_group()
	group.add_argument('-g', '--global', dest='globaltask', action='store_true',
			help='force use of users global todo.txt')
	group.add_argument('-l', '--local', dest='localtask', action='store_true',
			help='force use of users global todo.txt')
	
	parser.add_argument('command', metavar='<command>',
			choices=['add', 'a', 'do', 'list', 'ls'], default='ls', nargs='?', action='store')
	
	parser.add_argument('args', metavar='<args>', nargs='*', type=str,
                   help='an integer for the accumulator')

	args = parser.parse_args()

	if args.localtask:
		fileurl = 'todo.txt'
	elif args.globaltask:
		fileurl = '~/todo.txt'
	elif os.path.isfile('todo.txt'):
		fileurl = 'todo.txt'
	else:
		fileurl = '~/todo.txt'

	if args.command in ('ls','list'):
		list_tasks(fileurl)
	
	if args.command in ('add','a'):
		add_task(args.args, fileurl)
	
	if args.command == 'do':
		do_task(args.args, fileurl)
	

if __name__ == '__main__':
	main()