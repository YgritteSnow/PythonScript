# -*- coding: utf-8 -*- 

import json
import codecs
import csv

ENUM_TYPE_INT = 1
ENUM_TYPE_STRING = 2
ENUM_TYPE_LIST = 3
ENUM_TYPE_MAP = 4
ENUM_TYPE_FLOAT = 5
ENUM_TYPE_BOOL = 6

def GetDestpathAndOriginname(filename, destPath):
	dataName = filename.split('/')[-1].split('\\')[-1].split('.')[-2]
	filePath = filename[:filename.rfind(dataName)]
	if destPath is None:destPath = filePath

	return destPath, dataName

def SweepSpace(srcStr):
	srcStr = srcStr.encode('utf-8')
	i = len(srcStr) - 1
	print 'SweepSpace', srcStr, 
	while i >= 0:
		if srcStr[i] in ('\r', '\n', '\t', ',', ):
			i -= 1
		else:
			break
	print srcStr[:i+1]
	return srcStr[:i+1]

class CSVLoader(object):
	def __init__(self):
		super(CSVLoader, self).__init__()
		self.data_map = {} # 存储主表的数据
		self.data_summarySets = {} # 存储要统计的某一列 {col_name: value_ho}
		self.data_analyseMaps = {} # 存储要统计的某一列的 {col_name: {value:[key_value]} }

		self.destPath = ""
		self.dataName = ""

	def ZipData(self):return (self.data_map, self.data_summarySets, self.data_analyseMaps)

	def ParseAll(self, filename, destPath, summaryCol = ('key',), analyseCol = None):
		self.data_map = {} # 存储主表的数据
		self.data_summarySets = {} # 存储要统计的某一列 {col_name: value_ho}
		self.data_analyseMaps = {} # 存储要统计的某一列的 {col_name: {value:[key_value]} }
		self.Parse(filename, destPath)
		if summaryCol:self.ParseSummary(summaryCol)
		if analyseCol:self.ParseAnalyse(analyseCol)

		return

	def Parse(self, filename, destPath, summaryCol = ('key',), analyseCol = None):
		'''
		读取文件，得到一个数据，使用func函数将数据写入文件。

		数据格式：
		map tableContent{
			key1:{tabName1:(int, 123), tabName2:(string, "asdf"), tabName3:(list, )},
		}
		@param func:输出的函数
		'''
		self.destPath, self.dataName = GetDestpathAndOriginname(filename, destPath)

		line_idx = -1

		dataStructName = []
		dataStructType = []
		dataList = []

		for line in csv.reader(codecs.open(filename, 'r')):
			while( line[-1] == ''):
				line.pop()

			line_idx += 1

			if line_idx == 0:
				continue
			elif line_idx == 1:
				dataStructName = line
			elif line_idx == 2:
				dataStructType = [ self.parseType(typeName) for typeName in line ]
			else:
				dataList.append(self.parseData(dataStructType, line))

		self.data_map = {}
		for data_line in dataList:
			new_data = {}
			for data_one, data_name in zip(data_line[1:], dataStructName[1:]):
				new_data[data_name] = data_one
			self.data_map[data_line[0]] = new_data

		return

	def ParseSummary(self, summaryCol):
		# 统计的某一列的数据
		self.data_summarySets = {}
		for col_name in summaryCol:
			if col_name == 'key':
				self.data_summarySets[col_name] = set(self.data_map.keys())
			else:
				self.data_summarySets[col_name] = set([i[col_name] for i in self.data_map.values()])

		return

	def ParseAnalyse(self, analyseCol):
		'''统计某一列与主键的关系'''
		self.data_analyseMaps = {}
		for col_name in analyseCol:
			if col_name == 'key':
				continue
			else:
				analyseMap = {}
				for key, values in self.data_map.iteritems():
					analyseMap.setdefault(values[col_name], []).append(key)
					self.data_analyseMaps[col_name] = analyseMap

		return

	def WriteByFunc(self, func):
		func(self.destPath, self.dataName, self.data_map, self.data_summarySets, self.data_analyseMaps)

		return

	def parseType(self, typeStr):
		if typeStr == "int":
			return ENUM_TYPE_INT
		elif typeStr == "float":
			return ENUM_TYPE_FLOAT
		elif typeStr == "string":
			return ENUM_TYPE_STRING
		elif typeStr == "list":
			return ENUM_TYPE_LIST
		elif typeStr == "map":
			return ENUM_TYPE_MAP
		elif typeStr == "bool":
			return ENUM_TYPE_BOOL
		else:
			raise ValueError, "parseType Error: Invalid Type[ " + typeStr + " ]"
			return ENUM_TYPE_STRING

	def parseData(self, typeList, dataLineStr):
		data = []
		for t, d in zip(typeList, dataLineStr):
			if t == ENUM_TYPE_INT:
				data.append(int(eval(d)))
			elif t == ENUM_TYPE_STRING:
				data.append(d)
			elif t == ENUM_TYPE_FLOAT:
				data.append(float(eval(d)))
			elif t == ENUM_TYPE_LIST:
				data.append(tuple(eval(d)))
			elif t == ENUM_TYPE_MAP:
				data.append(eval(d))
			elif t == ENUM_TYPE_BOOL:
				data.append(bool(eval(d)))
			else:
				raise ValueError, "parseData Error: Invalid Type[ " + t + ", " + d + " ]"
				data.append("")
		return data
		

	def ParseDummy(self, filename):
		'''
		读取文件，直接输出到控制台
		'''
		dataName = filename.split('/')[-1].split('\\')[-1].split('.')[-2]
		filePath = filename[:filename.rfind(dataName)]
		#lines = open(filename).readlines()
		#for line in codecs.open(filename, 'r', 'gb2312').readlines(100):
		#	print line.encode('utf-8')

		f = codecs.open(filePath + 'd_' + dataName + '.js', 'w', 'utf-8')
		for line in csv.reader(codecs.open(filename, 'r')):
			[f.write(l.decode('gb2312')) for l in line]
		f.close()


def WriteToJsFile(filePath, dataName, data_map, summarySets, analyseMaps):
	new_file_name = 'd_' + dataName
	f = codecs.open(filePath + new_file_name + '.js', 'w', 'utf-8')
	f.write('var ' + new_file_name +' = ')
	#f.write(json.dumps(data_map), indent=4)
	#json.dump(data_map, f, ensure_ascii=False) # 不能用这个
	res = json.dumps(data_map, ensure_ascii=False, indent=4)
	f.write(res.decode('gb2312'))
	f.write(';')

	for summaryName, summarySet in summarySets.items():
		f.write('\n\n')
		f.write('var ' + new_file_name + '_' + summaryName + '_ho = ')
		res = json.dumps(tuple(summarySet), ensure_ascii=False)
		f.write(res.decode('gb2312'))
		f.write(';')

	for analyseName, analyseMap in analyseMaps.items():
		f.write('\n\n')
		f.write('var ' + new_file_name + '_' + analyseName + '_map = ')
		res = json.dumps(analyseMap, ensure_ascii=False)
		f.write(res.decode('gb2312'))
		f.write(';')
		
	f.close()

	return

a = CSVLoader()

#a.ParseDummy(r"D:\MyProjects\PythonScript\PythonScripts\majiang_pattern.csv")

for filename in ('majiang_pattern', 'majiang_card', ):
	srcPath = r"D:\MyProjects\PythonScript\PythonScripts\\" + filename + r'.csv'
	dstPath = r"D:\MyProjects\CocosProject\test\src\\"

	analyseCol = None
	if filename == 'majiang_pattern':analyseCol = ('higherPattern',)

	a.ParseAll(srcPath, dstPath, analyseCol=analyseCol)
	a.WriteByFunc(WriteToJsFile)