# -*- coding: utf-8 -*- 

import xml.dom.minidom.parse
import csv


ENUM_SHAPE_BLOCK = 1
ENUM_SHAPE_LINE = 3

masterMap = {
	5:ENUM_SHAPE_BLOCK,
	2:ENUM_SHAPE_LINE,
	0:ENUM_SHAPE_BLOCK,
}

class VisioXmlConv(object):

	def __init__(self):
		super(VisioXmlConv, self).__init__()
		self.data = None
		self.destPath = ""
		self.dataName = ""

	def Parse(self, filename, destPath=None):
		'''
		读取文件，得到一个数据，使用func函数将数据写入文件。

		数据格式：
		map tableContent{
			key1:{tabName1:(int, 123), tabName2:(string, "asdf"), tabName3:(list, )},
		}
		@param func:输出的函数
		'''
		self.destPath, self.dataName = GetDestpathAndOriginname(filename, destPath)

		dom = xml.dom.minidom.parse(filename)

		shape_list = dom.getElementsByTagName('Pages')[0].getElementsByTagName("Shapes")[0].getElementsByTagName("Shape")

		for shape in shape_list:
			shape_type = masterMap[shape_list["Master"]]

		print 1