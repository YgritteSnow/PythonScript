# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     系统函数
# ---------------------------

import copy

####################################################
###
####################################################

MAX_WIDTH = 9999

####################################################
###
####################################################

def DEBUG_ERR(*args, **kwargs):
    if 1:
        print args
    else:
        raise Exception, str(args)

####################################################
###
####################################################

class IntVec2( object ):
	
	def __init__(self, x, y=None):
		super(IntVec2, self).__init__()
		if y is None:
			self._x, self._y = x
		else:
			self._x = x
			self._y = y

	def __eq__(self, b):return self._x == b._x and self._y == b._y
	def __hash__(self):return self._x + self._y * MAX_WIDTH
	def __str__(self):return "(" + str(self._x) + ", " + str(self._y) + ")"
	def __iter__(self):
		for i in (self._x, self._y):yield i

	@property
	def x(self):return self._x
	@property
	def y(self):return self._y

	def toTuple(self):return (self._x, self._y)
	def offset(self, (x, y)):return (self._x + x, self._y + y)

	def AddX(self, x):self._x += x
	def AddY(self, y):self._y += y

	def Area(self):return self._x * self._y

####################################################
###
####################################################

class IntVec3( object ):
	
	def __init__(self, x, y=None, z=None):
		super(IntVec3, self).__init__()
		if y is None:
			self._x, self._y, self._z = x
		else:
			self._x = x
			self._y = y
			self._z = z

	def __eq__(self, b):return self._x == b._x and self._y == b._y and self._z == b._z
	def __hash__(self):return self._x + self._y * MAX_WIDTH + self._z * MAX_WIDTH * MAX_WIDTH
	def __str__(self):return "(" + str(self._x) + ", " + str(self._y) + ", " + str(self._z) + ")"
	def __iter__(self):
		for i in (self._x, self._y, self._z):yield i

	def __div__(self, b):return IntVec3(self._x/b, self._y/b, self._z/b)
	def __mul__(self, b):return IntVec3(self._x*b, self._y*b, self._z*b)
	def __add__(self, b):return IntVec3(self._x+b._x, self._y+b._y, self._z+b._z)
	def __sub__(self, b):return IntVec3(self._x-b._x, self._y-b._y, self._z-b._z)

	@property
	def r(self):return self._x
	@property
	def g(self):return self._y
	@property
	def b(self):return self._y

	def toTuple(self):return (self._x, self._y, self._z)
	def addTuple(self, (x,y,z)):
		self._x += x
		self._y += y
		self._z += z

####################################################
###
####################################################

class SortAndFind_Vec3( object ):
	'''
	Vector3 的排序-查找器
	输入数据，生成一定的索引，以便快速查找

	支持：
	1. SortByLinear 线性索引，支持线性排序函数
	2. SortBySquare 八叉树索引，支持欧拉距离排序、曼哈顿距离排序等
	'''

	def __init__(self, objList):
		super(Sorter_Vec3, self).__init__()
		self._objList = objList

		self._linearBuff = None # 使用线性索引
		self._squareBuff = None # 使用八叉树索引

	#################################
	###
	#################################

	def SortByLinear(self, linearFunc):
		'''
		使用线性函数作为排序函数
		'''
		self._linearBuff = copy.deepcopy(self._objList)
		self._linearBuff.sort( key = linearFunc )

		return 


	def _finder_linear_repeat_y(self, color, repeatBuff):
		nearestIdx = self._finder_linear_repeat_x(color)
		if nearestIdx not in repeatBuff:return nearestIdx

		destValue = self._weightMethod_linear(color)

		lo = nearestIdx - 1
		hi = nearestIdx + 1
		while lo >= 0 or hi < len(self._linearBuff):

			if not hi < len(self._linearBuff):
				while lo in repeatBuff:lo -= 1
				if lo < 0:raise Exception, "Images is lack"

				return lo
			elif not lo >= 0:
				while hi in repeatBuff:hi += 1
				if hi >= len(self._linearBuff):raise Exception, "Images is lack"

				return hi

			if destValue - self._linearBuff[lo] < self._linearBuff[hi] - destValue:
				if lo in repeatBuff:
					lo -= 1
				else:
					return lo
			else:
				if hi in repeatBuff:
					hi += 1
				else:
					return hi

	def _finder_linear_repeat_x(self, color):
		destValue = self._weightMethod_linear(color)

		# 二分查找落在哪个区间
		lo = 0 # 左侧的哨兵
		hi = len(self._linearBuff) - 1 # 右侧的哨兵
		while hi - lo > 1:
			mid = (lo + hi) // 2
			if self._linearBuff[mid] > destValue:
				hi = mid
			else:
				lo = mid

		# if hi == len(self._linearBuff):return lo
		return hi if self._linearBuff[hi] - destValue < destValue - self._linearBuff[lo] else lo

	#################################
	###
	#################################

	def _find(self, obj, findFunc_repeat_x, findFunc_repeat_y, index_buff, repeatBuff=None):
		'''
		线性函数排序器所对应的查找
		'''
		if index_buff == None:
			raise Exception, "Have not initialised Linear Sorter!"

		if repeatBuff is None:
			return self._originImageList[findFunc_repeat_x(color)]
		else:
			index = findFunc_repeat_y(color, repeatBuff)
			repeatBuff.add(index)
			try:
				return self._originImageList[index]
			except:
				print "index out of range, ", index, len(self._originImageList), color
				print "index out of range, ", repeatBuff

			raise Exception, "FindMatchImage end"