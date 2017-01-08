# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     解析字符串的通用的函数
# ---------------------------

import copy

# 空字符
g_blankChar = ('\t', ' ', )

# 非数字和字母的字符
g_split_char = frozenset(('!', ' ', '#', '"', "'", '&', ')', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '>', '[', ']', '\\', '{', '}', '|', '~', '?', ))

##################################################################
### 分割字符串
##################################################################

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
### 注：只能查找一个双引号之间的内容
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
### 把目标字符串按照双引号内容分割，yield输出
### 注：每次输出内容为 双引号前的内容(包含前引号) 和 双引号内的内容
##################################################################

def deleteComments( origin_str, line_comment_str, section_comment_strs ):
	origin_str = copy.deepcopy(origin_str)
	match_comments = [(l, r) for l,r in section_comment_strs]
	match_comments.append((line_comment_str, "\n"))
	for comment_left, comment_right in match_comments:
		while True:
			idx_comment_left = origin_str.find(comment_left)
			if idx_comment_left == -1:
				break

			idx_comment_right = origin_str[idx_comment_left+1:].find(comment_right)

			#print "deleteComments ... ", idx_comment_left, idx_comment_right, origin_str[idx_comment_left:idx_comment_right]
			if idx_comment_right == -1:
				origin_str = origin_str[:idx_comment_left]
			else:
				idx_comment_right += idx_comment_left+1
				origin_str = origin_str[:idx_comment_left] + origin_str[idx_comment_right+1:]

	return origin_str

def splitByDoubleQuote( origin_str ):
	origin_str = deleteComments(origin_str, "//", (("/*", "*/"), ))
	cur_lo = -1
	cur_hi = -1

	cur_finding_min_idx = 0
	last_match_hi = 0

	_deep = 100
	while _deep > 0:
		_deep -= 1
		temp_find = origin_str[cur_finding_min_idx:].find("\"")
		if temp_find != -1:
			if temp_find != 0 and origin_str[temp_find-1] == "\\":
				# 对转义字符，继续向后查找( todo 这里其实不准确，因为前一个反斜杠也可能是已经被转义了的无效字符)
				cur_finding_min_idx = temp_find + 1
			else:
				if cur_lo == -1: # 优先查找左侧字符
					cur_lo = temp_find + cur_finding_min_idx
					cur_finding_min_idx = cur_lo + 1
				else:
					cur_hi = temp_find + cur_finding_min_idx
					cur_finding_min_idx = cur_hi + 1
					yield origin_str[last_match_hi:cur_lo+1], origin_str[cur_lo+1:cur_hi]
					last_match_hi = cur_hi
					cur_lo = -1 # 重置左侧字符为未查找状态
		else:
			break

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

##################################################################
### 去掉行前行后的字符串
##################################################################

def splitPreFix( line ):
	idx = 0
	while idx != len(line) and line[idx] in g_blankChar:idx += 1
	return line[:idx], line[idx:]

def splitPostFix( line ):
	idx = len(line) - 1
	while idx != -1 and line[idx] in g_blankChar:idx -= 1
	return line[:idx+1], line[idx+1:]

##################################################################
### 分割文件名字符串为path和filename两部分
##################################################################

def replaceStrByMatchedStr( originStr, matchStr, newStr ):
	if originStr.find(matchStr) != -1:
		match_lo = originStr.find(matchStr)
		match_hi = match_lo + len(matchStr)
		originStr = originStr[:match_lo] + newStr + originStr[match_hi:]

	return originStr