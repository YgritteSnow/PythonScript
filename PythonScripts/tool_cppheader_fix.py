# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     对给定目录或文件中的所有文件，如果是头文件，则考察其文件起始两行是否有头文件保护，没有的话就加上
#     假定第一个 "#ifndef" 和最后一个 "#endif" 一定是用来头文件保护的，也就是说没有用户定义的在那个位置的同名编译命令
# ---------------------------

import os
from lib_file_node import *
from lib_string_common import splitStr

def filepath_2_headerString( filepath ):
	pathwords = splitStr(filepath)

	res_str = '__'
	for word in pathwords:
		res_str += word.upper()
		res_str += '_'
	res_str += '_'

	return res_str

def fixPrefixByLines( filelines, prefixString ):
	# 先去除首位空行
	if len(filelines) == 0:
		pass
	else:
		old_len = -1
		while old_len != len(filelines):
			old_len = len(filelines)
			if( filelines[0] == '\n' ):filelines.pop(0)
			if( len(filelines) > 1 and filelines[1] == '\n' ):filelines.pop(1)
			if( len(filelines) and filelines[-1] == '\n' ):filelines.pop(-1)
	
	# 确保前两行是 ifndef 和 define
	if len(filelines) and filelines[0].startswith("#ifndef"):filelines.pop(0)
	filelines.insert(0, "#ifndef " + prefixString + '\n')
	
	if len(filelines) > 1 and filelines[1].startswith("#define"):filelines.pop(1)
	filelines.insert(1, "#define " + prefixString + '\n' )

	if len(filelines) and filelines[-1].startswith("#endif"):
		filelines.pop(-1)
		filelines.append( "#endif " )
	else:
		filelines.append( "\n#endif " )

def fixHeaderPrefix():
	print 'Fix Start'

	filelist = (
		r"F:\MyProjects\DxDemo_1\DxDemo_1",
	)
	for filetree_name in filelist:
		file_tree = FileTree(filetree_name)
		for file_node in file_tree.allFile():
			fullpath = file_node.fullDir
			if not fullpath.endswith( '.h' ):
				continue

			filestr = open( file_node.fullDir , 'r+' )
			try:
				f_lines = filestr.readlines( 100 )

				fixPrefixByLines( f_lines, filepath_2_headerString(file_node.fullDir[len(filetree_name)+1:]) )
				filestr.seek(0)
				filestr.close()

				filestr = open( file_node.fullDir , 'w+' )
				filestr.writelines( f_lines )
				filestr.close()
				
			except IOError:
				print 'IO error'
				pass
			filestr.close()

	print 'Fix end'

if __name__ == '__main__':
	fixHeaderPrefix()