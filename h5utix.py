"""
	Utilities for handling HDF5 files
"""
import h5py

_HEAD = None
_FILE = None

def open(filename, *arg):
	""" Open a HDF5 file """
	global _FILE, _HEAD
	_FILE = h5py.File(filename, *arg)
	_HEAD = _FILE
	return _FILE

def close():
	""" Close the current file """
	global _FILE, _HEAD
	if _FILE is not None:
		_FILE.close()
		_FILE = None
		_HEAD = None

def pwd():
	return _HEAD.name


def ls(grp=None, flag=None):
	global _HEAD
	if grp is None:
		grp = _HEAD
	if isinstance(grp, str): grp = get_group(grp)
	subgrps = [key for key in grp.keys()]
	return subgrps

def cd(grp=None):
	global _HEAD
	if grp is None: grp = _FILE
	if isinstance(grp, str): grp = get_group(grp)
	_HEAD = grp
	return grp

def mkdir(grp_name):
	global _FILE, _HEAD
	if grp_name[0]=='/': grp_cur = _FILE
	else grp_cur = _HEAD
	return grp_cur.create_group(grp_name)

def rm(grp):
	grp = get_group(grp)
	del grp

def touch(dset_name):
	pass


#=======================
#   Internal functions
#=======================

def get_group(grp_name):
	""" Return a group instance from string """
	global _FILE, _HEAD
	if grp_name=='/':
		return _FILE
	if grp_name=='.':
		return _HEAD
	if len(grp_name)>1 and grp_name[0]=='/':
		grp_path= grp_name[1:]
	else:
		grp_path = _HEAD.name + '/' + grp_name
	if grp_path in _FILE:
		return _FILE[grp_path]
	else:
		print("Error: Cannot find path. Return current group.")
		return _HEAD

def options(flg_str):
	""" Return a dictionary """
	flg_str = flg_str.lower()
	opts = {'r':False,	# Recursive
			'p':False,	# Print
			'a':False	# All
			}
	for k in opts.keys():
		if flg_str.find(k) > -1: opts[k] = True
	return opts

def filter_args(*args):
	""" Analyze the arguments """
	global _HEAD
	target = _HEAD.name
	flag = ""
	if len(args)>1:
		target = args[0]
		flag = flag.join([k for k in args[1:] if isinstance(k,str)])
	elif len(args)==1:
		if isinstance(args[0],str):
			flag = args[0]
			fs = flag.split()
			if fs[0][0].isalnum():
				target = fs[0]
				flag = "".join(fs[1:])
		else: target = args[0]
	return target, flag

def display(items, tree=False, info=False):
	""" Display a list of items """
	if not tree:
		for i,item in enumerate(items):
			print("{}  {}".format(i,item))
	else:
		items = sorted(items)
		for i,item in enumerate(items):
			compos = item.split('/')
			disp = ''
			for j in range(len(compos)-1):
				disp = disp + '|   '
			disp = disp + '|__ ' + compos[-1]
			# if disp[1]=='|': disp = disp[1:]
			print("{}  {}".format(i,disp))
