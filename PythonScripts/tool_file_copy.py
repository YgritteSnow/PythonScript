# -*- coding: utf-8 -*- 

###################################################
### 拷贝文件相关
### 使用方法：
### 	1. 拉到最下边，修改main函数里的相应的路径；
### 	2. AnalysisFileAndCopyResources_js_byStr 中的字符串中的内容会被遍历检查，
### 		如果发现双引号包裹的内容包含了res目录，那么
###################################################

import os.path
import shutil

from lib_string_common import replaceStrByMatchedStr, splitByDoubleQuote

# 需要复制过去的字段，按照优先级，例如Plist已经修改过了，那么Path就不改了
g_csdElements = ("Plist", "Path", )

# 获得某字段后边紧跟的那个双引号里边的内容 - 单个
def findSrcFileNameInLine_one(lineTxt, matchStr):
	p = lineTxt.find(matchStr + "=")
	if p == -1:
		return None 

	match_lo = lineTxt[p:].find("\"") + p + 1
	match_hi = lineTxt[match_lo:].find("\"") + match_lo
	return lineTxt[match_lo:match_hi]

# 获得某字段后边紧跟的那个双引号里边的内容 - 按照 g_csdElements 中配置的优先级得到最高的为准
def findSrcFileNameInLine_all(lineTxt):
	for ele in g_csdElements:
		res = findSrcFileNameInLine_one(lineTxt, ele)
		if res:
			return res

# 输入src路径、文件名，dest路径，执行拷贝
def copyFromFileToFile(srcPath, srcFile, destPath):
	if not os.path.isdir(destPath):
		os.makedirs(destPath)
	srcFilePath = os.path.join(srcPath, srcFile)
	destFilePath = os.path.join(destPath, srcFile)
	shutil.copy(srcFilePath, destFilePath)

# 生成目标文件路径
def generateDestFilePath(srcRelativeFilePath):
	if srcRelativeFilePath.find("res") != -1:
		idx_respath = srcRelativeFilePath.find("res")
		return os.path.join(
			os.path.join(srcRelativeFilePath[:idx_respath], "res/images_scmj")
			, srcRelativeFilePath[idx_respath+len("res/"):]
			)

	return os.path.join("images_scmj/", srcRelativeFilePath);

# 根据源文件目录、源文件相对路径、目标文件目录，得到目标文件相对路径
def getDestFilePathInfos(srcFilePathPrefix, srcRelativeFileName, destFilePathPrefix):
	srcRelativeFilePath = os.path.dirname(srcRelativeFileName)
	fileName = os.path.basename(srcRelativeFileName)

	srcFilePath_full = os.path.join(srcFilePathPrefix, srcRelativeFilePath)

	dstFilePath_relative = generateDestFilePath(srcRelativeFilePath)
	dstFilePath_full = os.path.join(destFilePathPrefix, dstFilePath_relative)

	return srcFilePath_full, fileName, dstFilePath_full, dstFilePath_relative

# 解析一个文件，替换其涉及的资源路径为新目录的资源路径，然后另存为新文件
def ModifySrcFile(
	originFileName, 
	newFileName,
	srcFilePathPrefix, 
	destFilePathPrefix
	):
	f = open(originFileName, 'r')
	f_lines_new = []
	while True:
		f_line = f.readline()
		if not f_line:break

		res = findSrcFileNameInLine_all(f_line)
		if res:
			srcRelativeFilePath = findSrcFileNameInLine_all(f_line)

			srcFilePath_full, fileName, dstFilePath_full, destFilePath_relative = getDestFilePathInfos(
				srcFilePathPrefix, srcRelativeFilePath, destFilePathPrefix)

			destFileName_relative = os.path.join(destFilePath_relative, fileName)
			new_line = replaceStrByMatchedStr(f_line, srcRelativeFilePath, destFileName_relative)
		else:
			new_line = f_line

		f_lines_new.append(new_line)
	f.close()

	dst = open(newFileName, 'w+')
	dst.writelines(f_lines_new)
	dst.close()

# 解析一个文件，对其中涉及的资源拷贝到新路径中
def AnalysisFileAndCopyResources_csd(
	originFileName, 
	newFileName,
	srcFilePathPrefix, 
	destFilePathPrefix
	):
	f = open(originFileName, 'r')
	while True:
		f_line = f.readline()
		if not f_line:break

		res = findSrcFileNameInLine_all(f_line)
		if res:
			srcRelativeFilePath = findSrcFileNameInLine_all(f_line)

			srcFilePath_full, fileName, dstFilePath_full, destFilePath_relative = getDestFilePathInfos(
				srcFilePathPrefix, srcRelativeFilePath, destFilePathPrefix)

			copyFromFileToFile( srcFilePath_full, fileName, dstFilePath_full )

			if fileName.endswith(".plist"):
				new_fileName = fileName[:-6] + ".png"
				copyFromFileToFile( srcFilePath_full, new_fileName, dstFilePath_full )
	f.close()

# 解析一个文件，对其中涉及的资源拷贝到新路径中，并修改本文件的路径为新路径，然后存储为新文件
def AnalysisSrcFileNameFromFileAndCopyToDestPathAndModifySrcFile(
	originFileName, 
	newFileName,
	srcFilePathPrefix, 
	destFilePathPrefix
	):
	AnalysisFileAndCopyResources_csd( originFileName, newFileName, srcFilePathPrefix, destFilePathPrefix )
	ModifySrcFile( originFileName, newFileName, srcFilePathPrefix, destFilePathPrefix )

# 静态分析代码工程中的所有文件，分析其包裹在单双引号内的所有资源，如果找到了该资源，那么拷贝到目标目录中
# （暂时先做成分析单个文件）
def AnalysisFileAndCopyResources_js(srcPath, srcFilePathPrefix, destFilePathPrefix):
	f = open(srcPath, 'r')
	while True:
		f_line = f.readline()
		if not f_line:break

		AnalysisFileAndCopyResources_js_byStr(f_line, srcFilePathPrefix, destFilePathPrefix)
	f.close()

def AnalysisFileAndCopyResources_js_byStr(origin_str, srcFilePathPrefix, destFilePathPrefix):
		for nullstr, srcRelativeFilePath in splitByDoubleQuote(origin_str):
			fullpath = os.path.join(srcFilePathPrefix, srcRelativeFilePath)
			if not os.path.isfile(fullpath):
				continue

			srcFilePath_full, fileName, dstFilePath_full, destFilePath_relative = getDestFilePathInfos(
				srcFilePathPrefix, srcRelativeFilePath, destFilePathPrefix)

			if fileName.find("res") != -1:
				print "ERROR: check by yourself for NON-'res/' resources! "
				continue

			if fileName.endswith(".json"):
				CopyJsonAndCsd( srcFilePathPrefix, fileName, destFilePathPrefix )
			else:
				CopySimpleImages( srcFilePath_full, fileName, dstFilePath_full )

def GetCsdByJson( jsonName, srcFilePathPrefix, destFilePathPrefix):
	csdName = jsonName.split(".")[0] + ".csd"
	srcPath = os.path.join(os.path.join(srcFilePathPrefix, "cocosstudio"), csdName)
	destPath = os.path.join(os.path.join(destFilePathPrefix, "cocosstudio"), csdName)
	return srcPath, destPath

# 拷贝json文件，需要拷贝其对应的csd文件
def CopyJsonAndCsd( srcFilePathPrefix, fileName, destFilePathPrefix ):
	srcFileName_full, dstFileName_full = GetCsdByJson(fileName, srcFilePathPrefix, destFilePathPrefix)
	if os.path.isfile(dstFileName_full):
		print 'ERROR: CSD file Conflicted:', srcFileName_full
		return

	AnalysisSrcFileNameFromFileAndCopyToDestPathAndModifySrcFile(
		srcFileName_full, 
		dstFileName_full, 
		os.path.join(srcFilePathPrefix, 'cocosstudio'),
		os.path.join(destFilePathPrefix, 'cocosstudio'),
		)

# 拷贝简单资源，只需要直接拷贝过去
def CopySimpleImages( srcFilePath_full, fileName, dstFilePath_full ):
	if os.path.isfile(dstFilePath_full + fileName):
		print 'ERROR: Image file Conflicted:', srcFileName_full
		return
	copyFromFileToFile( srcFilePath_full, fileName, dstFilePath_full )


# 对游戏代码中运行时生成的log（生成函数见注释），使用此函数进行分析，对使用到的资源，拷贝到目标目录
# （暂时放一放，先看上边的够不够用）
# （事实证明貌似够用……）
def AnalysisAndCopy_dynamic():pass

if __name__ == "__main__":

		# AnalysisSrcFileNameFromFileAndCopyToDestPathAndModifySrcFile(
		# 	r"D:\WorkProjects\scmj\ccclient\cocosstudio\endAll.csd",
		# 	r"D:\WorkProjects\gsmj\ccclient\cocosstudio\endAll_sc.csd",
		# 	r"D:\WorkProjects\scmj\ccclient\cocosstudio",
		# 	r"D:\WorkProjects\gsmj\ccclient\cocosstudio"
		# 	)

		AnalysisFileAndCopyResources_js_byStr(
			r'''
	Player_Type_Info_2fan:"res/playtypeinfo/2fan.png",
	Player_Type_Info_3fan:"res/playtypeinfo/3fan.png",
	Player_Type_Info_4fan:"res/playtypeinfo/4fan.png",
	Player_Type_Info_tc_out:"res/playtypeinfo/tc_03.png",
	Player_Type_Info_tc_in:"res/playtypeinfo/tc_05.png",
	Player_Type_Info_tc_19:"res/playtypeinfo/tc_19.png",
	Player_Type_Info_dgh_dp:"res/playtypeinfo/dgh_dp.png",
	Player_Type_Info_dgh_zm:"res/playtypeinfo/dgh_zm.png",
	Player_Type_Info_mqzz:"res/playtypeinfo/mqzz.png",
	Player_Type_Info_tdh:"res/playtypeinfo/tdh.png",
	Player_Type_Info_dph:"res/playtypeinfo/dph.png",
	Player_Type_Info_zmh:"res/playtypeinfo/zmh.png",

	Player_Type_Info_YaoJiu:"res/playtypeinfo/yaojiujiangdui.png",
	Player_Type_Info_JiaDi:"res/playtypeinfo/zimojiadi.png",
	Player_Type_Info_ZiMoJiaFan:"res/playtypeinfo/zimojiafan.png",
	Player_Type_Info_kxh:"res/playtypeinfo/kxh.png",
	Player_Type_Info_bkxh1:"res/playtypeinfo/bkxh1.png",
	Player_Type_Info_jxw:"res/playtypeinfo/jxw.png",
	Player_Type_Info_ytl:"res/playtypeinfo/ytl.png",
	Player_Type_Info_xzdd:"res/playtypeinfo/xzdd.png",
	Player_Type_Info_yjd:"res/playtypeinfo/yjd.png",
	Player_Type_Info_hjzy:"res/playtypeinfo/hjzy.png",
	Player_Type_Info_hjzyzg:"res/playtypeinfo/hjzyzg.png"
			''',
			r"D:\WorkProjects\scmj\ccclient",
			r"D:\WorkProjects\gsmj\ccclient"
			)

		# AnalysisFileAndCopyResources_js_byStr(
		# 	r"D:\WorkProjects\gsmj\ccclient\Play_sc.js",
		# 	r"D:\WorkProjects\hnmjRelease\ccclient",
		# 	r"D:\WorkProjects\gsmj\ccclient"
		# 	)