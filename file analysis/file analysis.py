# -*- coding:utf-8 -*-
import os

#----------------------------
g_file_postfix = ('.cpp', '.h', '.ipp', )

g_split_char = ('!', ' ', '#', '"', "'", '&', ')', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '>', '[', ']', '\\', '{', '}', '|', '~', '?', )

g_split_re = '[!#&)(+*-,/.;:=<>}|~]'

g_wordchar = frozenset(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', '', 'v', 'w', 'x', 'y', 'z', 
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', '', 'V', 'W', 'X', 'Y', 'Z', 
	'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', ))

#----------------------------
# 对单词的限制

g_ifIgnoreSysWord = True 
g_word = frozenset((
	'const', 'void', 'virtual', 'class', 'varient', 'public', 'private', 'protected', 'static', 
	'if', 'return', 'else', 'for', 'this', 'break', 'endif', 'ifdef', 'ifndef', 'define', 'case', 'new', 'iterator', 'delete', 'struct', 
	'int', 'char', 'bool', 'std', 'string', 'c_str', 'push_back', 'size', 'end', 'begin', 'type', 'clear', 'empty', 'append', 'size_t', 
	'h','float', 
	'true', 'false', 'NULL', 'i', ))
def ifSysWord(string):return string in g_word


g_ifIgnoreDigit = True 		# 是否忽略数字
def ifDigit(string):return string.isdigit()

g_ifIgnoreTooShort = 4 		# 忽略多长以下的字符串
def ifTooShort(string):return len(string) < g_ifIgnoreTooShort

g_ifIgnoreTooLong = 20 		# 忽略多长以上的字符串
def ifTooLong(string):return len(string) > g_ifIgnoreTooLong

g_ifPrefixUpper = False 		# 忽略首字母非大写
def ifPrefixUpper(string):return not string[0].isupper()

g_restrictConfig_word = ( 						# 二者都为 true 则排除该单词
	(g_ifIgnoreSysWord, ifSysWord), 		# 系统
	(g_ifIgnoreDigit, ifDigit), 			# 数字
	(g_ifIgnoreTooShort, ifTooShort), 		# 过短
	(g_ifIgnoreTooLong, ifTooLong), 		# 过长
	(g_ifPrefixUpper, ifPrefixUpper), 		# 首字母大写
)

#--------------------------
# 对文件读取过程中的排除

g_restrictConfig_line = (
)
#--------------------------
##################################################################
class FileNode(object):

	def __init__(self, namestr, fatherpath):
		super(FileNode, self).__init__()
		self._name = namestr
		self._path = fatherpath
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
		assert self._isFile

	def allNode(self):return (self, )
	def allFile(self):return (self, )
	def allDir(self):return (self, )


class FileTree(FileNode):

	def __init__(self, pathstr):
		super(FileTree, self).__init__('', pathstr)
		assert self._isDir

		self._isFile = False
		self._isDir = True
		self._children = []

		self._queryChildren()
	@property 
	def fullDir(self):return self._path

	def _queryChildren(self):
		t_fnStack = [self, ]

		count = 0
		while t_fnStack:

			t_node = t_fnStack.pop()
			count += 1
			t_path = t_node.fullDir
			for t_childname in os.listdir(t_path):
				t_newnode = FileNode(t_childname, t_path)
				t_node.addChild(t_newnode)

				if t_newnode.isDir:
					t_fnStack.append(t_newnode)
		print 'File count: ', count

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

def ifCareFile(filename):
	for postfix in g_file_postfix:
		if filename.endswith(postfix):
			return True
	return False

##################################################################
def splitStr(string):
	res = string.split()
	for split_char in g_split_char:
		new_res = []
		for s in res:
			new_res.extend(s.split(split_char))
		res = new_res
	return res

##################################################################
def analysisUnwordchar(file_tree):
	unwords = set()
	for fnode in file_tree.allFile():
		fname = fnode.fullDir
		if not ifCareFile(fname):continue
		f = open(fname, 'r')

		try:
			f_str = f.read()#.decode('utf-8')
			for t_c in f_str:
				if t_c not in g_wordchar and ord(t_c) <= 127 and ord(t_c) >= 32:
					unwords.add(t_c)

			print unwords

		finally:
			f.close()


def analysisWord(file_tree):
	anares = {}
	for fnode in file_tree.allFile():
		fname = fnode.fullDir
		if not ifCareFile(fname):continue
		f = open(fname, 'r')

		try:
			f_str = f.read()#.decode('utf-8')
			for string in splitStr(f_str):
				if string not in anares:anares[string] = 0
				anares[string] += 1

		finally:
			f.close()

	return anares

##################################################################
def printSort_print(analysisRes):
	idx = 100
	for i, j in sorted(analysisRes.iteritems(), key=lambda a:a[1], reverse=True):
		print i,j

		idx -= 1
		if idx < 0:break

def printSort_file(analysisRes, writefilename):
	idx = 1000
	f = open(writefilename, 'w')
	try:
		for i, j in sorted(analysisRes.iteritems(), key=lambda a:a[1], reverse=True):

			ifContinue = False
			for chk_cfg, chk_func in g_restrictConfig_word:
				if chk_cfg and chk_func(i):
					ifContinue = True
					break
			if ifContinue:continue
				
			f.write(i + ' - ' + str(j) + '\n')

			idx -= 1
			if idx < 0:break
	finally:
		f.close()

def doFileMerge():
	print 'Query Start'

	filelist = (
		r"F:\MyProjects\DXSamples\CreateDevice", 
		r"F:\MyProjects\DXSamples\Vertices", 
		r"F:\MyProjects\DXSamples\Matrices", 
		r"F:\MyProjects\DXSamples\Lights", 
	)
	output_filename = r"F:\MyProjects\DXSamples\t.txt"

	old_words = []

	for old_filename in filelist[:-1]:
		file_tree = FileTree(old_filename)
		ana_res = analysisWord(file_tree)
		old_words.extend(ana_res.keys())

	new_file_tree = FileTree(filelist[-1])
	new_ana_res = analysisWord(new_file_tree)

	for nw in new_ana_res.keys():
		if nw in old_words:
			new_ana_res.pop(nw)

	printSort_file(new_ana_res, output_filename)

	print 'Query End'

#doFileMerge()

def doFileAnalisys():
	print 'Query Start'

	filelist = (
		r"E:\X5_2\depot\products\Project_X52\components\system_bonus\core\x5_bonus_player_service.cpp", 
	)
	output_filename = r"F:\t.txt"

	ana_res = {}

	for old_filename in filelist:
		file_tree = FileNodeTree(old_filename)
		temp_ana_res = analysisWord(file_tree)
		for word, count in temp_ana_res.iteritems():
			if word not in ana_res:ana_res[word] = 0
			ana_res[word] += count

	printSort_file(ana_res, output_filename)

	print 'Query End'

doFileAnalisys()