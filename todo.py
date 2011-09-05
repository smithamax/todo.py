#!/usr/bin/python
import argparse, re, os, ConfigParser as configparser
import fileinput, sys, datetime

def get_option(parser, section, option):
	try:
		value = parser.get(section, option)

	except configparser.NoSectionError:
		parser.add_section(section)
		value = get_option(parser, section, option)
	
	return value
	

def load_config(configfile='~/.todoconfig'):
	loc = {}
	glob = {}

	fix = os.path.expanduser

	parser = configparser.ConfigParser({'dir':'~','filename':'TODO','donefilename':'DONE'})
	parser.read(fix(configfile))


	glob['dir'] = fix(get_option(parser, 'global', 'dir'))
	glob['filename'] = fix(get_option(parser, 'global', 'filename'))
	glob['donefilename'] = fix(get_option(parser, 'global', 'donefilename'))


	loc['filename'] = fix(get_option(parser, 'local', 'filename'))
	loc['donefilename'] = fix(get_option(parser, 'local', 'donefilename'))
	loc['dir'] = os.getcwd();

	return glob, loc




def parsetask(line):
	done, line = parsedone( line )

	if re.match(r'\A *[\-xX ] ', line):
		line = re.sub(r'\A *[\-xX ] ', "", line)

	return done, line

def parsedone(line):
	done = False

	if re.match(r'\A *[xX] ', line):
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


def removedone(furl, linenums):
	for line in fileinput.input(furl, inplace=1):
		if fileinput.filelineno() in linenums:
			line = ""
		
		sys.stdout.write(line)




class Task(object):
	"""docstring for Task"""
	def __init__(self, line, lineno):
		self.done, self.task = parsetask(line)
		self.line = lineno

		self.subtasks = []


def add_task(args, furl):
	f = open(furl, 'a')
	if len(args): 
		f.write('- '+str.join(' ',args)+'\n')
	else:
		print 'Add Mode (leave field blank to quit)'
		while True:
			tasktext = raw_input('add> ')
			tasktext = tasktext.strip()
			if tasktext.lower() in ('done', '', 'quit', 'exit'):
				break
			
			f.write('- '+tasktext+'\n')

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

def archive_tasks(options):
	furl = os.path.join(options['dir'], options['filename'])
	doneurl = os.path.join(options['dir'], options['donefilename'])
	f = open(furl, 'r')
	tasklist = parsefile(f)
	f.close()
	donelist = []
	date = datetime.date.today()
	datestr = date.strftime('%d-%b-%Y')

	#make done list
	for t in tasklist:
		if t.done:
			donelist.append(t)
	
	#add done to done.txt
	f = open(doneurl, 'a')
	for t in donelist:
		f.write(datestr +' '+ t.task + '\n')
	f.close()

	#remove done from todo.txt
	nums = []
	for t in donelist:
		nums.append(t.line)
	removedone(furl, nums)







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
	
	group.add_argument('-g', '--global',
			dest='globaltask',
			action='store_true',
			help='force use of users global todo.txt'
			)

	group.add_argument('-l', '--local',
			dest='localtask',
			action='store_true',
			help='force use of directories local todo.txt'
			)

	parser.add_argument('command',
			metavar='<command>',
			choices=['add', 'a', 'do', 'list', 'ls', 'archive'],
			default='ls', nargs='?',
			action='store'
			)
	
	parser.add_argument('args',
			metavar='<args>',
			nargs='*', type=str,
			help='depends on command'
			)

	args = parser.parse_args()

	glob, loc = load_config()
	if os.path.isfile('.todo'):
		dontcare, loc = load_config('.todo')
	
	options = {}

	if args.localtask:
		options = loc
	elif args.globaltask:
		options = glob
	elif os.path.isfile(loc['filename']):
		options = loc
	else:
		options = glob

	path = os.path.join(options['dir'], options['filename'])
	if not os.path.isfile(path):
		f = open(path, 'w')
		f.close()

	if args.command in ('ls','list'):
		list_tasks(path)
	
	if args.command in ('add','a'):
		add_task(args.args, path)
	
	if args.command == 'do':
		do_task(args.args, path)

	if args.command == 'archive':
		archive_tasks(options)
	

if __name__ == '__main__':
	main()
