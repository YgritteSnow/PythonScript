# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     将给定的像素尽力拼合成给定的图形
# ---------------------------

import os
import pygame
import Image

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

	def __div__(self, b):
		self._x /= b
		self._y /= b
		self._z /= b

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

########################################################################
###
########################################################################

class ImageJointMosaicNode( object ):

	def __init__(self, slicePiece, destImageObj):
		super(ImageJointMosaicNode, self).__init__()

		self._destColor = None
		self._sliceSize, self._slicePos = slicePiece

	def _calDatas(self, destImageObj):
		pixel_sum = IntVec3(0, 0, 0)
		count = 0

		sizex, sizey = destImageObj.size()
		x_min, x_max = self._slicePos.x, self._slicePos.x + self._sliceSize.x
		y_min, y_max = self._slicePos.y, self._slicePos.y + self._sliceSize.y
		x_min = max(0, x_min)
		y_min = max(0, y_min)
		x_max = min(sizex, x_max)
		y_max = min(sizey, y_max)
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				pixel_sum.addTuple(im.getpixel((x,y)))
				count += 1

		pixel_sum /= count

		self.destColor = pixel_sum

	@property 
	def destColor(self):return self._destColor
	@property 
	def slicePos(self):return self._slicePos
	@property 
	def sliceSize(self):return self._sliceSize

########################################################################
###
########################################################################

class ImageJointSrcImageNode( object ):

	def __init__(self, imagePath):
		super(ImageJointSrcImageNode, self).__init__()

		self._color = None
		self._calDatas(imagePath)

	def _calDatas(self, imagePath):
		originImage = Image.open(imagePath)
		pixel_sum = IntVec3(0, 0, 0)
		count = 0

		for x in range(0, im.size[0]):
			for y in range(0, im.size[1]):
				pixel_sum.addTuple(originImage.getpixel((x,y)))
				count += 1
		pixel_sum /= count

		self._color = pixel_sum

	@property 
	def averageColor(self):return self._color

########################################################################
###
########################################################################

class ImageJointMosaic( object ):
	'''
	计算出一个良好的方案，将给定的若干张图片放入切分好了的目标图片中，尽可能的模拟目标图片的效果
	'''

	def __init__(self, srcImageList, sliceData, destImage):
		super(ImageJointMosaic, self).__init__()

		self._originImageList = [] # 经过处理的图片的列表
		self._destMosaicNodes = [] # 经过处理的目标马赛克节点的列表
		self.SetMosaicData(srcImageList, sliceData, destImage) # 初始化所需的数据

		 # RGB通道的权重计算式
		 # 注意：只支持线性的式子，否则会出现排序错误
		self._weightMethod = lambda color:color.r + color.g + color.a

	####################################################
	###
	####################################################

	def SetMosaicData(self, srcImageList, sliceData, destImage):
		self._originImageList = [] # 经过处理的图片的列表
		self._originImageValueList = [] # 图片的权重值的列表
		self._destMosaicNodes = [] # 经过处理的目标马赛克节点的列表

		for imagePath in srcImageList:
			self._originImageList.append(ImageJointSrcImageNode(imagePath))

		self._originImageList.sort(key=lambda node:self._weightMethod(node.averageColor))
		self._originImageValueList = [self._weightMethod(node.averageColor) for node in self._originImageList]

		destImageObj = Image.open(destImage)
		for slicePiece in sliceData:
			self._destMosaicNodes.append(ImageJointMosaicNode(slicePiece, destImageObj))

		return

	####################################################
	###
	####################################################

	def ProcessMosaic(self):
		self._showVisualResult(self._processMosaic())

		return

	def _processMosaic(self, useOrderedMargin=False, canRepeat=True):
		'''
		填充马赛克区域
		@param useOrderedMargin: 是否使用顺序的累加器来累加误差。如果开启的话，建议目标填充物是按照顺序的（或者至少相邻两个在位置上是接近的）
		@param canRepeat: 是否可以重复选择同一图片
		@return: 计算结果的图片的列表
		'''
		result = []

		repeatBuff = set() if canRepeat else None # 缓存中存储的是图片的index

		last_color_surplus = 0 # 上一次模拟时的颜色的剩余（已经乘以了面积）
		for slice_node in self._destMosaicNodes:
			cur_dest_color = slice_node.destColor
			if useOrderedMargin:cur_dest_color += last_color_surplus / slice_node.sliceSize.Area()

			find_src_img = self.FindMatchImage(cur_dest_color, repeatBuff)
			result.append( find_src_img )

			last_color_surplus = ( cur_dest_color - find_src_img.Color() ) * find_src_img.Area()

		return result

	####################################################
	###
	####################################################

	def FindMatchImage(self, color, repeatBuff=None):
		if repeatBuff is None:
			return self._originImageList[self._findMatchImage_repeat_x(color)]
		else:
			index = self._findMatchImage_repeat_y(color, repeatBuff)
			repeatBuff.add(index)
			return self._originImageList[index]

	def _findMatchImage_repeat_y(self, color, repeatBuff):
		nearestIdx = self._findMatchImage_repeat_x(color)
		if nearestIdx not in repeatBuff:return nearestIdx

		destValue = self._weightMethod(color)

		lo = nearestIdx - 1
		hi = nearestIdx + 1
		while lo >= 0 or hi < len(self._originImageValueList):

			if not hi < len(self._originImageValueList):
				while lo in repeatBuff:lo -= 1
				return lo
			elif not lo >= 0:
				while hi in repeatBuff:hi += 1
				return hi

			if destValue - self._originImageValueList[lo] < self._originImageValueList[hi] - destValue:
				if lo in repeatBuff:
					lo -= 1
				else:
					return lo
			else:
				if hi in repeatBuff:
					hi += 1
				else:
					return hi

	def _findMatchImage_repeat_x(self, color):
		destValue = self._weightMethod(color)

		# 二分查找落在哪个区间
		lo = 0 # 左侧的哨兵
		hi = len(self._originImageValueList) - 1 # 右侧的哨兵
		while hi - lo > 1:
			mid = (lo + hi) // 2
			if self._originImageValueList[mid] > destValue:
				hi = mid
			else:
				lo = mid

		# if hi == len(self._originImageValueList):return lo
		return hi if self._originImageValueList[hi] - destValue < destValue - self._originImageValueList[lo] else lo

	####################################################
	###
	####################################################
	
	def _showVisualResult(self, resultImg):
		pygame.init()
		screen = pygame.display.set_mode(self.surSize, 0, 32)
		screen.fill((255, 255, 255))

		for mosaicNode, imageNode in zip(self._destMosaicNodes, resultImg):
			pygame.draw.rect(screen, imageNode.color.toTuple(), (mosaicNode.slicePos.toTuple(), mosaicNode.sliceSize.toTuple()), 0)

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

