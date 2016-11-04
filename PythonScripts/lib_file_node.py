# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     建立文件树
# ---------------------------

import os

##################################################################
class FileNode(object):

	def __init__(self, namestr, fatherpath):
		super(FileNode, self).__init__()
		self._name = namestr
		no_slash_idx = len(fatherpath) - 1
		while fatherpath[no_slash_idx] == '\\' or fatherpath[no_slash_idx] == '/':
			no_slash_idx -= 1

		self._path = fatherpath[:no_slash_idx+1]

		self._isFile = os.path.isfile(fatherpath + '/' + namestr)
		self._isDir = os.path.isdir(fatherpath + '/' + namestr)
		self._children = []

	@property 
	def isFile(self):return self._isFile
	@property 
	def isDir(self):return self._isDir
	@property 
	def fullDir(self):return self._path + '/' + self._name
	@property
	def name(self):return self._name

	@property 
	def children(self):return self._children

	def addChild(self, fn):self._children.append(fn)

class FileNodeTree(FileNode):

	def __init__(self, filename):
		idx_min = filename.find('/')
		idx_max = filename.find('\\')
		if idx_min == -1 and idx_max != -1:
			pass
		elif idx_min != -1 and idx_max == -1:
			idx_min, idx_max = idx_max, idx_min
		elif idx_min != -1 and idx_max != -1:
			idx_min, idx_max = min(idx_min, idx_max), max(idx_min, idx_max)
		path = filename[:idx_max]
		name = filename[idx_max+1:]

		super(FileNodeTree, self).__init__(name, path)

	def allNode(self):return (self, )
	def allFile(self):return (self, )
	def allDir(self):return (self, )


class FileTree(FileNode):

	def __init__(self, filename):
		if os.path.isdir(filename):
			super(FileTree, self).__init__('', filename)
			self._queryChildren()

		else:
			idx_min = filename.rfind('/')
			idx_max = filename.rfind('\\')
			if idx_min == -1 and idx_max != -1:
				pass
			elif idx_min != -1 and idx_max == -1:
				idx_min, idx_max = idx_max, idx_min
			elif idx_min != -1 and idx_max != -1:
				idx_min, idx_max = min(idx_min, idx_max), max(idx_min, idx_max)
			path = filename[:idx_max]
			name = filename[idx_max+1:]
			super(FileTree, self).__init__(name, path)

	def _queryChildren(self):
		t_fnStack = [self, ]

		count = 0
		while t_fnStack:

			t_node = t_fnStack.pop()
			if t_node._isFile:continue

			t_path = t_node.fullDir
			for t_childname in os.listdir(t_path):
				t_newnode = FileNode(t_childname, t_path)
				t_node.addChild(t_newnode)
				count += 1

				if t_newnode.isDir:
					t_fnStack.append(t_newnode)

		print 'NodeCount ', count

	def allNode(self):
		t_fnStack = [self, ]
		while t_fnStack:
			t_node = t_fnStack.pop()
			yield t_node
			t_fnStack.extend(t_node.children)

	def allFile(self):
		for node in self.allNode():
			if node.isFile:
				yield node

	def allDir(self):
		for node in self.allNode():
			if node.isDir:
				yield node
