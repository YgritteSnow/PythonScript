# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     遍历所有 .cpp 和 .h 文件，在 include 处，将所有引号括起来的类，重新设置为正确的目录。
#     主要用于，手动随意的拖拽文件位置之后，修复 include 的关联
#     假定：
#          所有文件路径不会有恰好和根目录同名的目录名
#          所有文件名均唯一
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
### 将所有的 include 修复
### 函数：fixIncludes()
##################################################################

def filepath_2_includeStr( filepath ):
	res_include = '#include \"'
	res_include += filepath_correct( filepath )
	res_include += '\"\n'
	return res_include

def filepath_2_filename( includeStr ):
	pathwords = splitStr( includeStr, ('\"', '\\', '/', ) )
	print 'filepath_2_filename' , pathwords
	i = len(pathwords) - 1
	while i >= 0:
		if len(pathwords[i]):
			return pathwords[i]
		i -= 1
	return ''

def fixIncludes( fullpath, t_file_map ):
	if not ifCareFile( fullpath ):return

	print 'fix includes start', fullpath

	filestr = open( fullpath, 'r+' )
	try:
		f_lines = []

		lines = filestr.readlines( readline_max )
		while len(lines):
			tochangelines = []
			for idx, line in enumerate(lines):
				if line.startswith( "#include" ):
					tochangelines.append( idx )

			for idx in tochangelines:
				line = lines[idx]
				include_name = filepath_2_filename(line)
				if include_name not in t_file_map:continue

				newline = filepath_2_includeStr( t_file_map[include_name] )
				lines[idx] = newline
			f_lines.extend( lines )

			lines = filestr.readlines( readline_max )

		filestr.close()

		filestr = open( fullpath , 'w+' )
		filestr.writelines( f_lines )
		
	except IOError:
		print 'IO error'
		pass

	filestr.close()

	print 'fix includes end'

##################################################################
### 将 .vcxproj, .filters 修复
### 函数：fixIncludes()
##################################################################

def fixVcxprojs( fullpath, t_file_map ):
	if not ifCareFile( fullpath, ('.vcxproj', '.vcxproj.filters', ) ):return

	print 'fix vcxprojs start', fullpath

	filestr = open( fullpath, 'r+' )

	f_lines = []
	try:
		print 'filename ', fullpath
		lines = filestr.readlines( readline_max )
		while len(lines):
			print 'line count ', len(lines)
			for line in lines:
				if line.find("Include=") != -1:
					h_file_name = findHFilename( line )
					new_h_file_name = t_file_map.get( h_file_name )

					if new_h_file_name:
						new_file_path = filepath_correct( new_h_file_name )

						f_lines.append( replaceStrInQuot( line, new_file_path ) )
					else:
						f_lines.append( line )
				else:
					f_lines.append( line )

				if line.find("源文件") != -1:
					# 看了下这个貌似没法手动替换，所以 filter 的替换还是编辑器里边手动吧
					pass

			lines = filestr.readlines( readline_max )

		filestr.close()

		filestr = open( fullpath , 'w+' )
		filestr.writelines( f_lines )
		
	except IOError:
		print 'IO error'
		pass

	filestr.close()

	print 'fix vcxprojs end'

##################################################################
### 总函数
##################################################################

def reconstitution():
	print 'Fix Start'

	filelist = (
		r"F:\MyProjects\SimpleBMP_hzy\SimpleBMP\SimpleBMP", 
	)

	t_file_map = {}

	for filetree_name in filelist:
		file_tree = FileTree(filetree_name)
		for file_node in file_tree.allFile():
			fullpath = file_node.fullDir
			if not ifCareFile( fullpath ):continue

			if is_nonBuildin_headerfile( fullpath ) or is_nonBuildin_cppfile( fullpath ):
				t_file_map[file_node.name] = file_node.fullDir

	for filetree_name in filelist:
		file_tree = FileTree(filetree_name)
		for file_node in file_tree.allFile():
			fullpath = file_node.fullDir

			fixIncludes( fullpath, t_file_map )
			fixVcxprojs( fullpath, t_file_map )

	print 'Fix End'

reconstitution()
