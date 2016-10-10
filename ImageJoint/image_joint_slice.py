# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#	 图片处理框架
#	 切割图片部分
# ---------------------------

import pygame
import random
from image_joint_common import *
import copy

MAX_WIDTH = 9999

Enum_PushResult_Fail = 1
Enum_PushResult_End = 2
Enum_PushResult_Success = 3

Enum_ShowRowList = 1
Enum_ShowSliceData = 2

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

class ImageSlicer( object ):
	'''
	输入图片的大小和书目，得到合适的图片切割方案
	0. 输入的内容为“图片大小”到“该大小的图片数量”的字典
	1. 将所有图片依次放入目标面板中，放置的位置为最小高度的地方
	2. 如果没有可以放入该高度的地方
	'''

	def __init__(self, destSize, imagesInfo=[]):
		super(ImageSlicer, self).__init__()
		self._destSize = IntVec2(destSize)
		self.clearData()

	def clearData(self):
		self._rowList = [IntVec2(0, 0), ] # [(左下角坐标，宽度), ]
		self._sliceData = []

	def GetSliceRowList(self):return self._rowList
	def GetSliceData(self):return self._sliceData
	def pushSliceData(self, sliceSize, slicePos):self._sliceData.append((sliceSize, slicePos))
	def popSliceData(self):self._sliceData.pop()

	####################################################
	###
	####################################################

	def getNeedWidth(self):
		'''获得下一个准备放置的位置'''
		minHeight = MAX_WIDTH
		idx = -1
		for t_idx, pos in enumerate(self._rowList):
			if pos.y < minHeight:
				minHeight = pos.y
				idx = t_idx

		if idx == -1:
			raise Exception, "getNeedWidth failed"
		else:
			pos = self._rowList[idx]
			if idx == len(self._rowList) - 1:
				needWidth = self._destSize.x - pos.x
			else:
				needWidth = self._rowList[idx+1].x - pos.x

			return pos, needWidth, idx

	def rowPop(self, popSize, popPosX):
		if popPosX < 0:
			DEBUG_ERR("Invalid pop x")
			return

		idx = -1
		for t_idx, pos in enumerate(self._rowList):
			if pos.x > popPosX:
				idx = t_idx
				break

		if idx < 0:# 没有找到，说明在最后切割
			idx = len(self._rowList)
			nextX = self._destSize.x
		else:
			nextX = self._rowList[idx].x

		if idx == 0:
			# 这意味着self._rowList里边有数据且第一个数据就比popPos大，这是不可能的，因为self._rowList从0开始；
			# 或者意味着，self._rowList为空，这也是错误的
			raise Exception, "Poping From Nothing"

		if nextX < popPosX + popSize.x:
			DEBUG_ERR("Cant Pop(for Test)")
			return

		lastpos = self._rowList[idx-1]
		if lastpos < popSize.y:
			DEBUG_ERR("Pop to positive value")
			return

		self._rowList.insert(idx, IntVec2(popPosX, lastpos.y - popSize.y))
		self._rowList.insert(idx + 1, IntVec2(popPosX + popSize.x, lastpos.y))

		self.simpRowList(idx + 1)
		self.simpRowList(idx)

		self.popSliceData()

		return

	def rowPush(self, pushSize):
		'''
		增加一个方块，如果成功，返回True和信息，否则返回False和None
		'''
		if pushSize.x == 0:
			DEBUG_ERR("Invalid size x")
			return Enum_PushResult_Fail, None

		(needPosX, minHeight), needWidth, idx = self.getNeedWidth()

		if idx == -1:
			print "cannot put into dest" # 指示压栈尝试错误，需要弹出
			return Enum_PushResult_Fail, None
		if minHeight >= self._destSize.y:
			print "slice end" # 指示递归终点
			return Enum_PushResult_End, None

		newPos = IntVec2(needPosX, minHeight + pushSize.y)
		if needWidth == pushSize.x:# 恰好与将要放置的位置的宽度相等
			self._rowList[idx] = newPos
		elif needWidth > pushSize.x:# 如果容许的空间大于将要放置的位置的宽度
			self._rowList[idx] = newPos
			# 如果右侧没有完全超出的话，附加进去
			if needPosX+pushSize.x < self._destSize.x:
				self._rowList.insert(idx+1, IntVec2(needPosX+pushSize.x, minHeight))
		elif idx == len(self._rowList) - 1:# 如果在最右侧，那么不论如何容许放置
			self._rowList[idx] = newPos
		else:
			DEBUG_ERR("didnot match")
			return Enum_PushResult_Fail, None

		self.simpRowList(idx)
		self.pushSliceData(pushSize, IntVec2(needPosX, minHeight))

		return Enum_PushResult_Success, needPosX

	def simpRowList(self, idx):
		cur_y = self._rowList[idx].y
		cur_x = self._rowList[idx].x
		if len(self._rowList) <= 1:
			return

		while idx < len(self._rowList) - 1: # 向后查找能不能合并
			t_right = self._rowList[idx+1]
			if cur_x == t_right.x:
				self._rowList.pop(idx)
				break
			elif cur_y == t_right.y:
				self._rowList.pop(idx+1)
			else:
				break

		while idx > 0: # 向前查找能不能合并
			t_left = self._rowList[idx-1]
			if cur_x == t_left.x:
				self._rowList.pop(idx-1)
				break
			elif cur_y == t_left.y:
				self._rowList.pop(idx)
				idx -= 1
			else:
				break

		return

	####################################################
	###
	####################################################

	def GenerateSlicer(self, imagesInfo, usageRate = 0.9):
		'''递归压栈和回退，得到误差范围内的一个可行的方案：
		@param imageInfo: {图片大小:该大小的数量, }
		@param usageRate: 所给的图片使用了超过usage百分比，即结束，意味着给定图片不足。如果强行要每个图片都用上的话，时间复杂度会太大
		'''
		imageInfo = copy.deepcopy(imagesInfo)
		originImageCount = 0
		for i in imagesInfo.values():originImageCount += i

		self.clearData()

		maxwidth = self._destSize.x
		t_stack = []  # [(开始尝试时的idx，尝试的size, 尝试的idx偏移, 尝试的pos),]
		sizes = imagesInfo.keys()
		sizesCount = len(sizes)

		startIdx = random.randint(0, sizesCount)
		currentIdx = 0
		while( True ):
			# 从所有图片中随机选择一个作为下一个起始尝试目标，然后依次遍历所有可尝试的目标，来寻找解决方案
			# 如果没有找到，那么将上一次的选择pop出去，再继续尝试下一个

			(t_x, minHeight), needWidth, t_idx = self.getNeedWidth()

			# 当最小高度达到所需高度的时候结束
			if minHeight >= self._destSize.y:
				print "SUCCESS!"
				for i,j in imagesInfo.items():print "(", i, ",", j, ")"
				print "len_sliceData = ", len(self._sliceData)
				break

			while( currentIdx < sizesCount ):
				imageSize = sizes[(currentIdx + startIdx)%sizesCount]

				if imagesInfo[imageSize] > 0:
					pushResult, rowPos = self.rowPush(imageSize)
					if pushResult == Enum_PushResult_Success:
						t_stack.append((startIdx, imageSize, currentIdx, rowPos))
						imagesInfo[imageSize] -= 1 # 把用到的那个方块拿出池子
					
						startIdx = random.randint(0, sizesCount)
						currentIdx = 0

						break

				currentIdx += 1

			if currentIdx == sizesCount:
				if len(t_stack) == 0: # 没有找到解
					raise Exception, "no solution found"
				
				last_startIdx, last_size, last_sizeIdx, last_pos = t_stack.pop(-1)
				self.rowPop(last_size, last_pos)
				imagesInfo[last_size] += 1 # 把原先用到的方块放回池子

				currentIdx = last_sizeIdx + 1
				startIdx = last_startIdx

			curImageCount = 0
			for i in imagesInfo.values():curImageCount += i
			if originImageCount * (1-usageRate) >= curImageCount:
				print "images is too less:"
				for i,j in imagesInfo.items():print "(", i, ",", j, ")",
				print ""
				raise Exception, "images is too less"

####################################################
###
####################################################

class TestImageSlice( object ):

	def __init__(self):
		super(TestImageSlice, self).__init__()
		self.imgSize = (400, 200)
		self.surSize = (410, 210)
		self._fillColors = []

	def _showRowList(self, screen, rowListData):
		screen.fill((255, 255, 255))
		for idx in range(len(rowListData)-1):
			pos = rowListData[idx]
			width = rowListData[idx+1].x - pos.x
			pygame.draw.line(screen, (0, 0, 255), pos.toTuple(), pos.offset((width, 0)))
			pygame.draw.line(screen, (0, 0, 255), pos.toTuple(), (pos.x, 0))
			pygame.draw.line(screen, (0, 0, 255), pos.offset((width, 0)), (pos.x + width, 0))

		if len(rowListData) > 0:
			pos = rowListData[-1]
			width = self.imgSize[0] - pos.x
			pygame.draw.line(screen, (0, 0, 255), pos.toTuple(), pos.offset((width, 0)))
			pygame.draw.line(screen, (0, 0, 255), pos.toTuple(), (pos.x, 0))
			pygame.draw.line(screen, (0, 0, 255), pos.offset((width, 0)), (pos.x + width, 0))

		pygame.display.update()

	def _showSliceData(self, screen, sliceData):
		screen.fill((255, 255, 255))
		while len(sliceData) > len(self._fillColors):
			self._fillColors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

		for (sliceSize, slicePos), color in zip(sliceData, self._fillColors):
			pygame.draw.rect(screen, color, (slicePos.toTuple(), sliceSize.toTuple()), 0)

		pygame.display.update()

	def ShowVisualDataStepByStep(self, rowListData, showType = Enum_ShowRowList):
		t = ImageSlicer(self.imgSize)
		#t.rowPush(IntVec2(self.imgSize))
		pygame.init()
		screen = pygame.display.set_mode(self.surSize, 0, 32)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

				elif event.type == pygame.KEYDOWN:
					if rowListData:
						a, b, c = rowListData.pop()
						t.rowPush(IntVec2(a, b))

						if showType == Enum_ShowRowList:
							self._showRowList(screen, t.GetSliceRowList())
						elif showType == Enum_ShowSliceData:
							self._showSliceData(screen, t.GetSliceData())
					else:
						DEBUG_ERR("Done.")

	def ShowVisualDataOnce(self, imagesInfo):
		t = ImageSlicer(self.imgSize)
		pygame.init()
		screen = pygame.display.set_mode(self.surSize, 0, 32)
		t.GenerateSlicer(imagesInfo)
		self._showSliceData(screen, t.GetSliceData())
		print "2222"

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
		print "3333"


####################################################
###
####################################################

def main_test():
	testSlicer = TestImageSlice()

	testOpt = 2
	if testOpt == 1:
		# 逐步进行的测试模式
		# 随机生成一些数据来方便测试
		testNum3List = []
		for i in range(40):
			testNum3List.append((random.randint(1, 2) * 20, random.randint(1, 2) * 20, random.randint(1,6)*20))
		testSlicer.ShowVisualDataStepByStep(testNum3List, showType = Enum_ShowSliceData)

	elif testOpt == 2:
		# 直接输入得到解决结果的模式
		# 随机生成图片的数据的集合
		testImgList = {}
		for i in range(40):
			testImgList[IntVec2(10,20)] = 150
			testImgList[IntVec2(20,20)] = 150
			testImgList[IntVec2(20,10)] = 150
		testSlicer.ShowVisualDataOnce(testImgList)

main_test()