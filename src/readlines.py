#!/usr/bin/env pypy
# -*- coding: utf-8

import os

# file_path = '/Users/qwe/workspace/proj/ma_shanxi3/src/hall/'
# file_path = '/Users/qwe/workspace/proj/ma_shanxi3/src/'
file_path = '/Users/qwe/workspace/proj/mahjong_common/src/'

def cleanArray(arr):
	isnull = True
	while isnull:
		try:
			arr.remove('')
		except Exception, e:
			isnull = False

def getLinesOfFile(name):
	p = os.popen('wc -l ' + name).read()
	arr = p.split(' ')
	cleanArray(arr)
	return int(arr[0])

def readFolders(path):
	lines_sum = 0
	for i in os.listdir(path):
		f_p = os.path.join(path,i)
		# print 'readFolders:', f_p
		if os.path.isfile(f_p):
			if i.find('DS_Store') == -1:
				lines_sum = lines_sum + getLinesOfFile(f_p)
		else:
			lines_sum = lines_sum + readFolders(f_p)
	return lines_sum
print readFolders(file_path)



