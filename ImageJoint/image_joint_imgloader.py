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

	def __init__(self, imagePath, destSize = (60,60)):
		super(ImageJointSrcImageNode, self).__init__()

		slash_idx = max(imagePath.rfind('/'), imagePath.rfind('\\'))
		dot_idx = imagePath.rfind('.')
		self._filename = imagePath[slash_idx+1:dot_idx]
		self._filepath = imagePath[:slash_idx]

		self._obj = Image.open(imagePath)
		#self._obj.thumbnail((self._obj.size[0]/thumbnailRate, self._obj.size[1]/thumbnailRate), Image.ANTIALIAS)
		self._obj.thumbnail(destSize, Image.ANTIALIAS)
		#self._obj.save(imagePath + ".thumbnail", "JPEG")

		self._color = self._calColor()
		self._size = self._calSize()

	def _calColor(self):
		pixel_sum = IntVec3(0, 0, 0)
		count = 0
		print "----------", self._obj.size

		for x in range(0, self._obj.size[0]):
			for y in range(0, self._obj.size[1]):
				pixel_sum.addTuple(tuple(self._obj.getpixel((x,y))))
				count += 1
		pixel_sum /= count

		return pixel_sum

	def _calSize(self):return IntVec2(self._obj.size)

	@property 
	def obj(self):return self._obj

	@property 
	def averageColor(self):return self._color

	@property 
	def imgSize(self):return IntVec2(self._obj.size)

	@property 
	def filename(self):return self._filename
	@property 
	def filepath(self):return self._filepath

########################################################################
###
########################################################################

class ImageJointLoader( object ):

	def __init__(self, folderPath):
		super(ImageJointLoader, self).__init__()
		self._folderPath = folderPath

	def _collectImages(self, folderPath):
		if not os.path.isdir(folderPath):
			raise Exception, "invalid folder!"
			return

		images = []

		folders = [folderPath, ]
		while len(folders) > 0:
			cur_folder = folders.pop()

			for iter_folder in os.listdir(cur_folder):
				full_path = cur_folder + '\\' + iter_folder

				if os.path.isdir(full_path):
					folders.append(full_path)
				else:
					images.append(full_path)

		return images

	def _transToImageObjs(self, imagePaths):
		res = []
		idx = 0
		l = float(len(imagePaths))
		for p in imagePaths:
			idx += 1
			print "process: ", idx / l
			res.append(ImageJointSrcImageNode(p))
		return res

	def _calImageSizes(self, imageNodes):
		statis = {}

		for node in imageNodes:
			statis.setdefault(node.imgSize, []).append(node)

		return statis

	def InitCache(self):
		cachePath = self._folderPath + "/_image_joint_cache/"
		if os.path.isdir(cachePath):
			os.rmdir(cachePath)
		os.mkdir(cachePath)

		self._imagePaths = self._collectImages(self._folderPath) # 存储所有图片路径
		self._imageNodes = self._transToImageObjs(self._imagePaths) # 存储所有图片结点
		self._imageSizeStatis = self._calImageSizes(self._imageNodes) # 统计图片的所有size的数量

		for sz, node_list in self._imageSizeStatis.iteritems():
			sx, sy = sz
			cacheImg = Image.new("RGBA", (sx * len(node_list), sy), (255,0,0))
			for idx, node in enumerate(node_list):
				cacheImg.paste(node.obj, (sx*idx, 0))

			cacheName = str(sx)+"_"+str(sy)+".jpg"
			cacheImg.save(cachePath + cacheName)
			#cacheImg.save("_image_joint_cachea.jpg")

def main_test():
	loader = ImageJointLoader(r"D:\MyProjects\PythonScript\PythonScripts\testimages")
	loader.InitCache()

if __name__ == "__main__":
	main_test()