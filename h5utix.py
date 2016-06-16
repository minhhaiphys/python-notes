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
	if grp is None:
		grp = _HEAD
	if isinstance(grp, str): grp = get_group(grp)
	subgrp = []
	for key in grp.keys():
		subgrp.append(key)
	return subgrp

def cd(grp=None):
	global _HEAD
	if grp is None: grp = _FILE
	if isinstance(grp, str): grp = get_group(grp)
	_HEAD = grp
	return grp.name


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