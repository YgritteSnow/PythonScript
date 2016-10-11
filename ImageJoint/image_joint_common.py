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

class Octree( object ):
	''' 
	N叉树（及其结点）
	'''
	maxheight = 0

	def __init__(self, obj, keyFuncs, objList, height = 0):
		super(Octree, self).__init__()
		self._children = {}
		self._obj = obj
		self._height = height

		if self._height > Octree.maxheight:
			Octree.maxheight = self._height
			print "Octree height max:", Octree.maxheight

		if objList is not None and len(objList) > 1:
			self._addChildren(objList, keyFuncs)

	def __getitem__(self, key_list):
		cur_obj = self
		while len(key_list) > 0:
			cur_obj = self._children[key_list.pop(0)]
		return cur_obj._obj
		
	def _cmp(self, obj1, obj2):return obj1 < obj2
	def _calKey(self, obj, keyFuncs):
		return tuple([self._cmp(keyFunc(self._obj), keyFunc(obj)) for keyFunc in keyFuncs])

	def GetObj(self):return self._obj

	def _addChildren(self, objList, keyFuncs):
		chidObjList = {}
		for obj in objList:
			chidObjList.setdefault(self._calKey(obj, keyFuncs), []).append(obj)

		for key, objList in chidObjList.iteritems():
			self._children[key] = Octree(objList[0], keyFuncs, objList[1:], self._height + 1)

		return

	def SearchIdx(self, obj, keyFuncs):
		cur_key_list = []
		self._searchChildren(obj, keyFuncs, cur_key_list)

		return cur_key_list

	def _searchChildren(self, obj, keyFuncs, cur_key_list):
		cur_key = self._calKey(obj, keyFuncs)
		if self._children.has_key(cur_key):
			cur_key_list.append(cur_key)
			self._children[cur_key]._searchChildren(obj, keyFuncs, cur_key_list)

####################################################
###
####################################################
Enum_SortStrategy_Linear = 1
Enum_SortStrategy_Octree = 2

class SortAndFind_Vec3( object ):
	'''
	Vector3 的排序-查找器
	输入数据，生成一定的索引，以便快速查找

	支持：
	1. SortByLinear 线性索引，支持线性排序函数
	2. SortByOctree 八叉树索引，支持三个分量分别单调变化的函数
	'''

	def __init__(self, objList):
		super(SortAndFind_Vec3, self).__init__()
		self._objList = objList

		self._indexedObjBuff = None # 使用线性索引
		self._squareBuff = None # 使用八叉树索引


	def is_less(self, obj1, obj2, func):return func(obj1) < func(obj2)
	def is_more(self, obj1, obj2, func):return func(obj1) >= func(obj2)
	def minus(self, a, b, func):return func(a) - func(b)

	#################################
	###
	#################################

	def SortByStrategy(self, func, strategy):
		self._strategy = strategy
		if strategy == Enum_SortStrategy_Linear:
			self.SortByLinear(func)
		elif strategy == Enum_SortStrategy_Octree:
			self.SortByOctree(func)

		return

	def Find(self, obj, repeatBuff):
		if self._strategy == Enum_SortStrategy_Linear:
			return self.FindByLinear(obj, repeatBuff)
		elif self._strategy == Enum_SortStrategy_Octree:
			return self.FindByOctree(obj, repeatBuff)

	#################################
	###
	#################################

	def SortByLinear(self, linearFunc):
		'''
		使用线性函数作为排序函数
		'''
		self._func = linearFunc
		self._indexedObjBuff = copy.deepcopy(self._objList)
		self._indexedObjBuff.sort( key = linearFunc )

		return 

	def _finder_linear_repeat_x(self, obj, repeatBuff):
		nearestIdx = self._finder_linear_repeat_y(obj)
		if nearestIdx not in repeatBuff:return nearestIdx

		lo = nearestIdx - 1
		hi = nearestIdx + 1
		while lo >= 0 or hi < len(self._indexedObjBuff):

			if not hi < len(self._indexedObjBuff):
				while lo in repeatBuff:lo -= 1
				if lo < 0:raise Exception, "Images is lack"

				return lo
			elif not lo >= 0:
				while hi in repeatBuff:hi += 1
				if hi >= len(self._indexedObjBuff):raise Exception, "Images is lack"

				return hi

			if self.minus(obj, self._indexedObjBuff[lo], self._func) < self.minus(self._indexedObjBuff[hi], obj, self._func):
				if lo in repeatBuff:
					lo -= 1
				else:
					return lo
			else:
				if hi in repeatBuff:
					hi += 1
				else:
					return hi

	def _finder_linear_repeat_y(self, obj):
		# 二分查找落在哪个区间
		lo = 0 # 左侧的哨兵
		hi = len(self._indexedObjBuff) - 1 # 右侧的哨兵
		while hi - lo > 1:
			mid = (lo + hi) // 2
			if self.is_less(obj, self._indexedObjBuff[mid], self._func):
				hi = mid
			else:
				lo = mid

		return hi if self.minus(self._indexedObjBuff[hi], obj, self._func) < self.minus(obj, self._indexedObjBuff[lo], self._func) else lo

	#################################
	###
	#################################

	def SortByOctree(self, squareFunc):
		''' 
		使用距离函数作为排序依据
		'''
		self._func = squareFunc
		keyFuncs = (
			lambda obj:obj[0].r, 
			lambda obj:obj[0].g, 
			lambda obj:obj[0].b, 
			)
		self._indexedObjBuff = Octree(self._objList[0], keyFuncs, self._objList[1:]) # 建立八叉树索引

	def _finder_octree_repeat_y(self, obj):
		keyFuncs = (
			lambda obj:obj[0].r, 
			lambda obj:obj[0].g, 
			lambda obj:obj[0].b, 
			)
		return self._indexedObjBuff.SearchIdx(obj, keyFuncs) 

	def _finder_octree_repeat_x(self, obj):
		nearestIdx = _finder_linear_repeat_y(self, obj)
		# todo 以后再做不重复型的查询
		return nearestIdx

	#################################
	###
	#################################

	def FindByLinear(self, obj, repeatBuff=None):return self._find(obj, self._finder_linear_repeat_y, self._finder_linear_repeat_x, repeatBuff)
	def FindByOctree(self, obj, repeatBuff=None):return self._find(obj, self._finder_octree_repeat_y, self._finder_octree_repeat_x, repeatBuff)

	def _find(self, obj, findFunc_repeat_y, findFunc_repeat_x, repeatBuff=None):
		'''
		线性函数排序器所对应的查找
		'''
		if self._indexedObjBuff == None:
			raise Exception, "Have not initialised Linear Sorter!"

		if repeatBuff is None:
			return self._indexedObjBuff[findFunc_repeat_y(obj)]
		else:
			index = findFunc_repeat_x(obj, repeatBuff)
			repeatBuff.add(index)
			try:
				return self._indexedObjBuff[index]
			except:
				print "index out of range, ", index, len(self._indexedObjBuff), obj
				print "index out of range, ", repeatBuff

			raise Exception, "FindMatchImage end"