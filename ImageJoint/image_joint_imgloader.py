# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     加载和初步处理图片
# ---------------------------

import os
import Image
from image_joint_common import DEBUG_ERR
from image_joint_common import IntVec3, IntVec2

########################################################################
###
########################################################################

class ImageJointSrcImageNode( object ):

	def __init__(self, imagePath):
		super(ImageJointSrcImageNode, self).__init__()

		self._obj = Image.open(imagePath)
		self._color = self._calColor()
		self._size = self._calSize()

	def _calColor(self):
		pixel_sum = IntVec3(0, 0, 0)
		count = 0

		for x in range(0, im.size[0]):
			for y in range(0, im.size[1]):
				pixel_sum.addTuple(self._obj.getpixel((x,y)))
				count += 1
		pixel_sum /= count

		return pixel_sum

	def _calSize(self):return IntVec2

	@property 
	def averageColor(self):return self._color

	@property 
	def imgSize(self):return IntVec2(self._obj.size)

########################################################################
###
########################################################################

class ImageJointLoader( object ):

	def __init__(self, folderPath):
		super(ImageJointLoader, self).__init__()

		self._imageSizeStatis = {} # 图片的统计信息

		self._imagePaths = self._collectImages(folderPath) # 存储所有图片路径
		self._imageNodes = self._transToImageObjs(self._imagePaths) # 存储所有图片结点
		self._imageSizeStatis = self._calImageSizes(self._imageNodes) # 统计图片的所有size的数量

	def _collectImages(self, folderPath):
		if not os.isdir(folderPath):
			raise Exception, "invalid folder!"
			return

		images = []

		folders = [folderPath, ]
		while len(folders) > 0:
			cur_folder = folders.pop()

			for iter_folder in os.listdir():
				full_path = cur_folder + '\\' + iter_folder

				if os.isdir(full_path):
					folders.append(full_path)
				else:
					images.append(full_path)

		return images

	def _transToImageObjs(self, imagePaths):return [ImageJointSrcImageNode(p) for p in imagePaths]

	def _calImageSizes(self, imageNodes):
		statis = {}

		for node in imageNodes:
			statis.setdefault(node.imgSize, 0)[node.imgSize] += 1

		return statis