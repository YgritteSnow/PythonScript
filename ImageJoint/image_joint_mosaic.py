# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     将给定的像素尽力拼合成给定的图形
# ---------------------------

import pygame
import Image
import random

from image_joint_common import IntVec3, IntVec2

########################################################################
###
########################################################################

class ImageJointMosaicNode( object ):

	def __init__(self, slicePiece, destImageObj):
		super(ImageJointMosaicNode, self).__init__()

		self._sliceSize, self._slicePos = slicePiece
		self._destColor = self._calColor(destImageObj)

	def _calColor(self, destImageObj):
		pixel_sum = IntVec3(0, 0, 0)
		count = 0

		sizex, sizey = destImageObj.size
		x_min, x_max = self._slicePos.x, self._slicePos.x + self._sliceSize.x
		y_min, y_max = self._slicePos.y, self._slicePos.y + self._sliceSize.y
		x_min = max(0, x_min)
		y_min = max(0, y_min)
		x_max = min(sizex, x_max)
		y_max = min(sizey, y_max)
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				pixel_sum.addTuple(destImageObj.getpixel((x,y)))
				count += 1

		pixel_sum /= count

		return pixel_sum

	@property 
	def destColor(self):return self._destColor
	@property 
	def slicePos(self):return self._slicePos
	@property 
	def sliceSize(self):return self._sliceSize

########################################################################
###
########################################################################

class ImageJointMosaic( object ):
	'''
	计算出一个良好的方案，将给定的若干张图片放入切分好了的目标图片中，尽可能的模拟目标图片的效果
	'''

	def __init__(self, srcImageList, sliceData, destSize, destImage):
		super(ImageJointMosaic, self).__init__()
		 # RGB通道的权重计算式
		 # 注意：只支持线性的式子，否则会出现排序错误
		self._weightMethod_linear = lambda color:color.r + 2 * color.g + color.b
		self._weightMethod_sqare = lambda color:color.r*color.r + color.g*color.g + color.b*color.b
		self._weightMethod_common = lambda color:color.r*color.r + color.g*color.g + color.b*color.b

		self._surSize = destSize

		self.SetMosaicData(srcImageList, sliceData, destImage) # 初始化所需的数据

	####################################################
	###
	####################################################

	def SetMosaicData(self, srcImageList, sliceData, destImage):
		self._originImageList = srcImageList # 要使用的大量图片的（颜色，标记）对
		self._originImageValueList = [] # 图片的权重值的列表
		self._destMosaicNodes = [] # 经过处理的目标马赛克节点的列表

		self._originImageList.sort(key=lambda node:self._weightMethod_linear(node[0]))
		self._originImageValueList = [self._weightMethod_linear(node[0]) for node in self._originImageList]

		destImageObj = Image.open(destImage)
		for slicePiece in sliceData:
			self._destMosaicNodes.append(ImageJointMosaicNode(slicePiece, destImageObj))

		return

	####################################################
	###
	####################################################

	def ShowProcessMosaic(self):
		self._showVisualResult(self._processMosaic())

		return

	def _processMosaic(self, useOrderedMargin=False, canNotRepeat=False):
		'''
		填充马赛克区域
		@param useOrderedMargin: 是否使用顺序的累加器来累加误差。如果开启的话，建议目标填充物是按照顺序的（或者至少相邻两个在位置上是接近的）
		@param canNotRepeat: 是否可以重复选择同一图片
		@return: 计算结果的图片的列表
		'''
		result = []

		repeatBuff = set() if canNotRepeat else None # 缓存中存储的是图片的index

		last_color_surplus = 0 # 上一次模拟时的颜色的剩余（已经乘以了面积）
		for slice_node in self._destMosaicNodes:
			cur_dest_color = slice_node.destColor

			if useOrderedMargin:cur_dest_color += last_color_surplus / slice_node.sliceSize.Area()

			find_src_img_node = self.FindMatchImage(cur_dest_color, repeatBuff)
			result.append( find_src_img_node )

			last_color_surplus = ( cur_dest_color - find_src_img_node[0] ) * slice_node.sliceSize.Area()

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
			try:
				return self._originImageList[index]
			except:
				print "index out of range, ", index, len(self._originImageList), color
				print "index out of range, ", repeatBuff

			raise Exception, "FindMatchImage end"

	def _findMatchImage_repeat_y(self, color, repeatBuff):
		nearestIdx = self._findMatchImage_repeat_x(color)
		if nearestIdx not in repeatBuff:return nearestIdx

		destValue = self._weightMethod_linear(color)

		lo = nearestIdx - 1
		hi = nearestIdx + 1
		while lo >= 0 or hi < len(self._originImageValueList):

			if not hi < len(self._originImageValueList):
				while lo in repeatBuff:lo -= 1
				if lo < 0:raise Exception, "Images is lack"

				return lo
			elif not lo >= 0:
				while hi in repeatBuff:hi += 1
				if hi >= len(self._originImageList):raise Exception, "Images is lack"

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
		destValue = self._weightMethod_linear(color)

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
		screen = pygame.display.set_mode(self._surSize, 0, 32)
		screen.fill((255, 255, 255))

		for mosaicNode, imageNode in zip(self._destMosaicNodes, resultImg):
			pygame.draw.rect(screen, imageNode[0].toTuple(), (mosaicNode.slicePos.toTuple(), mosaicNode.sliceSize.toTuple()), 0)
		pygame.display.update()

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

def main_test():
	imgColorList = []
	#for x in range(0, 255, 10):
	#	for y in range(0, 255, 10):
	#		for z in range(0, 255, 10):
	#			imgColorList.append((IntVec3(x,y,z), 0))


	for x in range(0, 255, 10):
		imgColorList.append((IntVec3(x,x,x), 0))

	#for i in range(0, 100):
	#	imgColorList.append((IntVec3(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)), 0))

	testImgList = {}
	for i in range(40):
		#testImgList[IntVec2(10,5)] = 15000
		testImgList[IntVec2(5,5)] = 150000
		#testImgList[IntVec2(5,10)] = 15000

	sizetuple = (400, 400)

	print "GenerateSlicer start"
	sliceObj = __import__("image_joint_slice").ImageSlicer(sizetuple)
	sliceObj.GenerateSlicer(testImgList)
	print "GenerateSlicer end"

	print "ShowProcessMosaic start"
	mosaicObj = ImageJointMosaic(imgColorList, sliceObj.GetSliceData(), sizetuple, "test.jpg")
	mosaicObj.ShowProcessMosaic()
	print "ShowProcessMosaic end"

if __name__ == "__main__":
	main_test()