# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     总体而言，是一个统计文件中英文单词频率的工具
#     可以在 g_restrictConfig_word 函数中修改和新增对词汇的要求；
#     doFileMerge()：输入一系列文件名（或目录名），输出最后一个文件（或目录）包含的单词，且前边所有文件都不包含的单词；
#     doFileAnalisys(): 输入一系列文件名（或目录名），统计所有文件里边的单词的词频
# ---------------------------

from lib_file_node import *
from lib_string_common import splitStr, ifCareFile

#----------------------------
# 对单词的限制

g_worldCountPerFile = 2000
g_sortedPrinted = 100

g_ifIgnoreSysWord = True 
g_word = set((
	'const', 'void', 'virtual', 'class', 'varient', 'public', 'private', 'protected', 'static', 
	'if', 'return', 'else', 'for', 'this', 'break', 'endif', 'ifdef', 'ifndef', 'define', 'case', 'new', 'iterator', 'delete', 'struct', 
	'int', 'char', 'bool', 'std', 'string', 'c_str', 'push_back', 'size', 'end', 'begin', 'type', 'clear', 'empty', 'append', 'size_t', 
	'h','float', 
	'true', 'false', 'NULL', 'i', ))

def ifSysWord(string):return string in g_word

g_ifOnlyCaredword = set(
	)
def ifNotCareWord(string):return string not in g_ifOnlyCaredword

g_ifIgnoreDigit = True 		# 是否忽略数字
def ifDigit(string):return string.isdigit()

g_ifIgnoreTooShort = 4 		# 忽略多长以下的字符串
def ifTooShort(string):return len(string) < g_ifIgnoreTooShort

g_ifIgnoreTooLong = 20 		# 忽略多长以上的字符串
def ifTooLong(string):return len(string) > g_ifIgnoreTooLong

g_ifPrefixUpper = True 		# 忽略首字母非大写
def ifPrefixUpper(string):return not string[0].isupper()

g_restrictConfig_word = ( 						# 二者都为 true 则排除该单词
	(g_ifIgnoreSysWord, ifSysWord), 		# 系统
	(g_ifOnlyCaredword, ifNotCareWord), 	# 限定范围
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

def analysisWordFromString(ana_str):
	anares = {}
	for string in splitStr(ana_str):
		if string not in anares:anares[string] = 0
		anares[string] += 1
	return anares

def analysisWord(file_tree):
	anares = {}
	i = g_worldCountPerFile
	for fnode in file_tree.allFile():
		if i < 0:break
		i -= 1

		fname = fnode.fullDir
		if not ifCareFile(fname, ('js',) ):continue
		f = open(fname, 'r')

		try:
			f_str = f.read()
			anares = analysisWordFromString(f_str)

		finally:
			f.close()

	return anares

##################################################################
def printSort_print(analysisRes):
	idx = g_sortedPrinted
	for i, j in sorted(analysisRes.iteritems(), key=lambda a:a[1], reverse=True):

		idx -= 1
		if idx < 0:break

def printSort_file(analysisRes, writefilename):
	idx = g_sortedPrinted
	f = open(writefilename, 'w')
	f.write('Start:\n')
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

def doFileMerge_1():
	'''
	输出最后一个文件比前边的文件多出的那些单词
	'''
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

def doFileMerge_2():
	'''
	输出在第一个文件范围内的单词中，后边的文件使用过的单词和频率
	'''
	print 'Query Start'

	filelist = (
		r"D:\WorkProjects\xyzjmj\server\GameCode.js", 
		r"D:\WorkProjects\xyzjmj\server", 
	)
	output_filename = r"D:\t.txt"

	word_range = []
	file_tree = FileTree(filelist[0])
	ana_res = analysisWord(file_tree)
	g_ifOnlyCaredword.update(ana_res.keys())

	res_map = {}
	for old_filename in filelist[1:2]:
		file_tree = FileTree(old_filename)
		res_map = analysisWord(file_tree)

	for old_filename in filelist[2:]:
		file_tree = FileTree(old_filename)
		new_map = analysisWord(file_tree)
		for i,j in new_map:
			res_map.setdefault(i, 0)[i] = j

	printSort_file(res_map, output_filename)

	print 'Query End'

def doFileMerge_3():
	'''
	输出在第一个文件范围内的单词中，后边的文件未使用到的单词和频率
	'''
	print 'Query Start'

	filelist = (
		r"E:\X5_2\depot\products\Project_X52\ui_components\ui_activity_wnd\activity\tui_activitydetail.h", 
		r"E:\X5_2\depot\products\Project_X52\ui_components\ui_activity_wnd\activity\tui_activitydetail.cpp", 
	)
	output_filename = r"F:\t.txt"

	file_tree = FileTree(filelist[0])
	ana_res = analysisWord(file_tree)
	full_set = set(ana_res.keys())

	for old_filename in filelist[1:]:
		file_tree = FileTree(old_filename)
		res_map = analysisWord(file_tree)
		full_set -= set(res_map.keys())

	new_res_map = {}
	for i in full_set:
		new_res_map[i] = 0
		
	printSort_file(new_res_map, output_filename)

	print 'Query End'

def doFileMerge_4():
	'''
	输出在某个字符串范围的单词中，后边的文件未使用到的单词和频率
	'''
	print 'Query Start'

	filelist = (
		r"""
	switch(type)
	{
	case ATE_Valentines_Have_Lover:
	case ATE_Valentines_No_Lover:
	case ATE_Kiss_Togeter:
		return GetUIWndValet();
		break;
	//case  ATE_SpringFestival_Gift:
	//case ATE_SpringFestival_Bless:
	/*case ATE_SpringFestival:
		return GetUIWndSpring();
		break;*/
	case ATE_QUEEN_CARD:
		return GetUIWndCard();
		break;
	case ATE_FoolsDay:
		return GetUIWndFool();
		break;
	case ATE_Christmas:
		return GetUIWndChristmas();
		break;
	case ATE_NpcMatch:
		return GetUIWndMidMonth();
		break;
	case ATE_LabourDay:
		return GetUILabourDay();
	case ATE_HappyLabourDay:
		return GetUIHappyLabour();
	case ATE_DragonBoat_Race:
	case ATE_DragonBoat_Zongzi:
		return GetUIDragonboatDay();
	case ATE_Chinese_Valentine:
	case ATE_Bridge_Meet:
		return GetUIWndMagpieFestival();
	case ATE_National_Day_Recruitment:
	case ATE_National_Day_Battle:
		return GetUIWndNationalDay();
	case ATE_Single_Counter_Attack:
	case ATE_Real_Love:
	case ATE_Single_Goodbye:
		return GetUIWndSignalsDay(type);
		break;
	case ATE_Match_Activity:
		return GetUIWndMatchActivity();
	case ATE_ROLL:
		return GetUIWndRollActivity();
	case ATE_PARKOUR:
	case ATE_TicketLottery:
		return NULL;
	case ATE_TeachersDay:
		return GetUIWndTeacherDay();
	case ATE_PVE_Anniversary:
		return GetUIWndPveAnniversary();
	case ATE_PVE_Christmas:
		return GetUIWndPveChristmas();
	case ATE_OneYuan_Lottery:
		return GetUIWndOneYuanLottery();
	case ATE_Cupid520:
		return GetUIWnd520();
	case ATE_Anniversary:
		return GetUIWndAnniversary();
	case ATE_QixiCruise:
		return GetUIWndQixiCruise();
	case ATE_MidAutumn_National:
		return GetUIWndPveNational();
	case ATE_ThanksGiving_2015:
		return GetUIWndTurkeyDay();
	case ATE_TenMillionClicks_One:
	case ATE_TenMillionClicks_Area:
		return GetUIWndCombo();
	case ATE_Christmas_Wish:
		return GetUIWndChristmasSnowmen();   
	case ATE_Monkey_Send_Peach:
		return GetUIWndSpring();
	case ATE_PVE_Carnival:
		return GetUIWndPveCarnival();
	case ATE_VALENTINE_MAIN:
		return GetUIWndValentins();
	case ATE_GirlsDay:
		return GetUIWndGirlsDay();
	case ATE_Adventure_Entertainment:
		return GetUIWndMonsterEncircle();
	case ATE_CHILD_DAY:
		return GetUIWndChildrensDay();
	case ATE_Anniversary_Main:
	case ATE_Anniversary_DressPalace:
	case ATE_Anniversary_OfferQueenGift:
	case ATE_Anniversary_QueenNewClothes:
	case ATE_Anniversary_AliChasedPeach:
	case ATE_Anniversary_Carnival:
		return GetUIWnd2ndAnniversary();
	case ATE_SuperStartCollege:
		return GetUiWndSuperStartCollege();
	case ATE_MidAutumn_Festival_Rabbit:
		return GetUIWndMidAutumn();""", 
		r"E:\X5_2\depot\products\Project_X52\components\system_bonus\shared\x5_system_bonus_info.h", 
	)
	output_filename = r"F:\t.txt"

	ana_res = analysisWordFromString(filelist[0])
	full_set = set(ana_res.keys())

	for old_filename in filelist[1:]:
		file_tree = FileTree(old_filename)
		res_map = analysisWord(file_tree)
		full_set -= set(res_map.keys())

	new_res_map = {}
	for i in full_set:
		new_res_map[i] = 0
		
	printSort_file(new_res_map, output_filename)

	print 'Query End'

def doFileAnalisys():
	'''
	输出在所有文件使用过的单词和频率
	'''
	print 'Query Start'

	filelist = (
		r"E:\X5_2\depot\products\Project_X52\ui_components\ui_common_use\include\tui_UI_Data_Define.h", 
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

if __name__ == '__main__':
	doFileMerge_2()
