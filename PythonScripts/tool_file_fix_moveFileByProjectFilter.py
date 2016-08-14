# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     分析vcxproj.filter文件，将真实文件修改为filter所定义的路径
#     修改vcxproj.filter和vcxproj文件，将其中文件路径修复
#     调用前边的include修复工具，将文件内include的路径修复
# ---------------------------

from lib_file_node import *
from lib_string_common import splitStr, ifCareFile, replaceStrInQuot, findHFilename

root_filepath = "DxDemo_1"

readline_max = 1000

##################################################################
### 几个公用的函数
##################################################################

def is_nonBuildin_headerfile( filename ):
	return filename.endswith( '.h' ) and filename.find( root_filepath ) != -1
def is_nonBuildin_cppfile( filename ):
	return filename.endswith( '.cpp' ) and filename.find( root_filepath ) != -1

def filepath_correct( filepath ):
	pathwords = splitStr( filepath, ('\\', '/', ) )
	
	# 剔除目录中的空目录名（多半是盘符那里连着两个斜杠引起的
	for idx, word in enumerate(pathwords):
		if not len(word):
			pathwords = pathwords[idx+1:]
			break

	# 剔除目录中 root_filepath 以左的部分
	old_len = -1
	while( old_len != len(pathwords) ):
		old_len = len(pathwords)
		for idx, word in enumerate(pathwords):
			if word == root_filepath:
				pathwords = pathwords[idx+1:]
				break

	res_include = ''
	for word in pathwords:
		res_include += word
		res_include += '/'
	res_include = res_include[:-1]

	return res_include

##################################################################
### 得到在最前边匹配所给字符串之间的字符串
##################################################################

def clampStr( origin_str, start_str, end_str ):
        idx_start = origin_str.find(start_str)
        if idx_start == -1:return ""
        idx_start += len(start_str)
        idx_end = origin_str.find(idx_start)
        if idx_end == -1:return ""
        return origin_str[idx_start, idx_end]

##################################################################
### 总函数
##################################################################

def reconstitution( proj_file_name ):
	print 'Fix Start'

	filter_file = open( proj_file_name + r".filters", 'r+' )
	proj_file = open( proj_file_name , 'r+' )
	try:
		filter_lines = filter_file.readlines( 1000 )

		for idx,line in enumerate(filter_lines):
                        if line.find("<ClCompile Include=") == -1: # 是filter的映射行
                                continue

                        origin_path = clampStr(line, '"', '"')
                        filter_path = clampStr(filter_lines[idx+1], 'Source Files', '<')
		
	except IOError:
		print 'IO error'
		pass
	
	filter_file.close()

	print 'Fix End'

reconstitution( r"C:\Users\j\Documents\Git Projects\MyDXExercises\MyDxExercises\MyDxExercises.vcxproj" )
