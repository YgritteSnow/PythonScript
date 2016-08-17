# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     修复所有空格的问题，例如逗号应当在左侧没有空格，而右侧有一个空格，等等
#
# 还存在的问题，暂时没有想到统一的解决方法：
#     '+', '-' 正负号与数字组合时
#     '(', ')' 在连续使用时
#     ':' 冒号对于c++而言连续使用代表其他意义
#     '=', '-', '>', '<' 等符号在c++中有更多组合
# ---------------------------

import os
from lib_file_node import *
from lib_string_common import ifCareFile, splitPreFix, splitPostFix

# 文件最大行数
file_max_line = 400

# 所有左边需要有一个空格的字符
g_all_needOneBlank_left = (')', ']', )
# 所有右边需要有一个空格的字符
g_all_needOneBlank_right = ('(', '[', ',', )
# 所有左边不需要空格的字符
g_all_needNoBlank_left = ('(', '[', ',', )
# 所有右边不需要空格的字符
g_all_needNoBlank_right = (')', ']', )
# 需要空格的数量 hard code 用
g_needOneBlank_count = 1
g_needNoBlank_count = 0

##################################################################
### 处理某一行，修复其空格
##################################################################

def fixBlanksForLine_left( line, char, blankCount ):
	'''
	line:原字符串
	blankCount:需要空格的数量，0代表不需要
	'''
	pre_line, line = splitPreFix(line)

	next_idx = line.rfind(char)
	while next_idx != -1 and next_idx > 0:
		curBlankCount = blankCount # 记录应该插入或删除多少个空格（由正负值表示）
		token_idx = next_idx - 1 # 查找应该在哪个位置插入或者删除空格
		while token_idx != -1 and line[token_idx] == ' ':
			curBlankCount -= 1
			token_idx -= 1

		if curBlankCount == 0: # 空格恰好
			pass
		elif curBlankCount < 0: # 空格太多
			line = line[:next_idx + curBlankCount] + line[next_idx:]
		elif curBlankCount > 0: # 空格太少
			line = line[:next_idx] + ' ' * curBlankCount + line[next_idx:]

		old_idx = next_idx
		next_idx = line[:next_idx - blankCount].rfind(char)

	return pre_line + line

def fixBlanksForLine_right( line, char, blankCount ):
	'''
	line:原字符串
	blankCount:需要空格的数量，0代表不需要
	'''
	line, post_line = splitPostFix(line)
	#print '000', line, '111', post_line, '222'

	next_idx = line.find(char)
	while next_idx != -1 and next_idx < len(line) - 1:
		curBlankCount = blankCount # 记录应该插入或删除多少个空格（由正负值表示）
		token_idx = next_idx + 1 # 查找应该在哪个位置插入或者删除空格
		while token_idx != len(line) and line[token_idx] == ' ':
			curBlankCount -= 1
			token_idx += 1

		if curBlankCount == 0: # 空格恰好
			pass
		elif curBlankCount < 0: # 空格太多
			line = line[:next_idx+1] + line[next_idx+1 - curBlankCount:]
		elif curBlankCount > 0: # 空格太少
			line = line[:next_idx+1] + ' ' * curBlankCount + line[next_idx+1:]

		new_idx = line[next_idx + blankCount + 1:].find(char)
		if new_idx != -1:
			next_idx = new_idx + next_idx + blankCount + 1
		else:
			next_idx = -1

	return line

def fixBlanksForLine( line ):
	line.decode('utf-8')
	for char in g_all_needNoBlank_right:
		line = fixBlanksForLine_right( line, char, g_needNoBlank_count )
	for char in g_all_needNoBlank_left:
		line = fixBlanksForLine_left( line, char, g_needNoBlank_count )
	for char in g_all_needOneBlank_right:
		line = fixBlanksForLine_right( line, char, g_needOneBlank_count )
	for char in g_all_needOneBlank_left:
		line = fixBlanksForLine_left( line, char, g_needOneBlank_count )
	#line.encode('utf-8')
	return line

##################################################################
### 处理文件夹内所有文件
##################################################################

def fixBracketBlanks():
	print 'Fix Start'

	filelist = (
		r"F:\aaa",
	)
	for filetree_name in filelist:
		file_tree = FileTree(filetree_name)
		for file_node in file_tree.allFile():
			fullpath = file_node.fullDir
			print fullpath
			if not ifCareFile(fullpath, ('.py', '.cpp', '.h', )):
				continue

			filestr = open( file_node.fullDir , 'r+' )
			try:
				f_lines = filestr.readlines( file_max_line )

				for line_idx in range( len(f_lines) ):
					f_lines[line_idx] = fixBlanksForLine(f_lines[line_idx])

				filestr.close()

				filestr = open( file_node.fullDir , 'w+' )
				filestr.writelines( f_lines )
				filestr.close()
				
			except IOError:
				print 'IO error'
				pass
			filestr.close()

	print 'Fix end'


def test():
	filelist = (
		r"F:\aaa",
	)
	for filetree_name in filelist:
		file_tree = FileTree(filetree_name)
		for file_node in file_tree.allFile():
			fullpath = file_node.fullDir
			print fullpath
			if not ifCareFile(fullpath, ('.py', '.cpp', '.h', )):
				continue

			filestr = open( file_node.fullDir , 'r+' )
			try:
				line = filestr.readline()
				line.decode('gbk')
				print line

				filestr.close()
				
			except IOError:
				print 'IO error'
				pass
			filestr.close()

def test2():
	s = u"啊啊啊"
	print s
	
if __name__ == '__main__':
	fixBracketBlanks()
