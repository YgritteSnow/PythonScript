# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     解析字符串的通用的函数
# ---------------------------

##################################################################
### 分割字符串
##################################################################

g_split_char = frozenset(('!', ' ', '#', '"', "'", '&', ')', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '>', '[', ']', '\\', '{', '}', '|', '~', '?', ))

def splitStr(string, char_set = None):
	res = string.split()
	
	if char_set is None:char_set = g_split_char

	for split_char in char_set:
		new_res = []
		for s in res:
			new_res.extend(s.split(split_char))
		res = new_res
	return res

##################################################################
### 检查文件名后缀是否是所要的后缀
##################################################################

g_file_postfix = frozenset(('.cpp', '.h', '.ipp', ))

def ifCareFile(filename, strset = None):
	if strset is None:strset = g_file_postfix

	for postfix in strset:
		if filename.endswith(postfix):
			return True
	return False

##################################################################
### 检查所有不合法的字符，可以用作split的参考
##################################################################

g_wordchar = frozenset(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', '', 'v', 'w', 'x', 'y', 'z', 
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', '', 'V', 'W', 'X', 'Y', 'Z', 
	'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', ))

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

##################################################################
### 检查字符串中双引号内部的部分，如果包含所要的字符串，那么就把引号之间的部分替换为新的字符串
##################################################################

def replaceStrInQuot( origin_str, quote_new_str, left_quote = '"', right_quote = '"' ):
	l_idx = origin_str.find(left_quote)
	r_idx = origin_str.rfind(right_quote)
	if l_idx >= r_idx:return

	# 包含了左双引号的部分
	res_str = origin_str[:l_idx + 1]

	# 双引号之间的部分
	middle_str = origin_str[l_idx+1:r_idx]
	res_str += quote_new_str

	# 包含了右双引号的部分
	res_str += origin_str[r_idx:]

	return res_str

def findHFilename( origin_str ):
	res = splitStr( origin_str, ('.', '\\', '/', '"', ) )
	for postfix in ('h', 'cpp', ):
		try:
			t = res.index(postfix)
			return res[t-1] + '.' + postfix
		except:
			continue

##################################################################
### 匹配成对的字符串，例如括号、if/ifdef/endif
### 可能有左侧可匹配右侧的任意一个的，所以左右都用集合表示
##################################################################

def matchCaseWithWords( origin_str, left_cases, right_cases ):
	'''
		@param 
			origin_words: 输入的单词的列表，需要直接匹配后边的需求
	'''
	left_idx = 0
	right_idx = len(origin_words) - 1

	res = []
	while left_idx < right_idx:
		while origin_words[left_idx] not in left_cases and left_idx < right_idx:left_idx += 1
		while origin_words[right_idx] not in right_cases and left_idx < right_idx:right_idx += 1

		if left_idx >= right_idx:
			return res
		else:
			res.append( (left_idx, right_idx) )
			left_idx += 1
			right_idx += 1