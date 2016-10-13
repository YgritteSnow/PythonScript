# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     加载和初步处理图片
# ---------------------------

import os
import Image
from image_joint_common import DEBUG_ERR
from image_joint_common import IntVec3, IntVec2
import time

########################################################################
###
########################################################################

class ImageJointSrcImageNode( object ):

	def __init__(self, imagePath, destSize = (60,60)):
		super(ImageJointSrcImageNode, self).__init__()
		if not imagePath:return

		slash_idx = max(imagePath.rfind('/'), imagePath.rfind('\\'))
		dot_idx = imagePath.rfind('.')
		self._filename = imagePath[slash_idx+1:dot_idx]
		self._filepath = imagePath[:slash_idx]

		self._obj = Image.open(imagePath)
		#self._obj.thumbnail((self._obj.size[0]/thumbnailRate, self._obj.size[1]/thumbnailRate), Image.ANTIALIAS)
		self._obj.thumbnail(destSize, Image.ANTIALIAS)
		self._obj = self._obj.resize(destSize)
		#self._obj.save(imagePath + ".thumbnail", "JPEG")

		self._color = self._calColor()
		self._size = self._calSize()

	@staticmethod
	def generateByImgObj(obj, destSize = (60,60)):
		res = ImageJointSrcImageNode('', destSize)
		res._obj = obj
		res._color = res._calColor()
		res._size = res._calSize()
		return res

	########################################################################
	###
	########################################################################

	def _calColor(self):
		pixel_sum = IntVec3(0, 0, 0)
		count = 0

		for x in range(0, self._obj.size[0]):
			for y in range(0, self._obj.size[1]):
				pixel_sum.addTuple(list(self._obj.getpixel((x,y)))[:3])
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

	_cacheName = "_image_joint_cache"

	def __init__(self, folderPath, forceSize=(60,60)):
		super(ImageJointLoader, self).__init__()
		self._folderPath = folderPath
		self._forceSize = forceSize

	########################################################################
	###
	########################################################################

	def InitCache(self):
		cachePath = os.path.join(self._folderPath, ImageJointLoader._cacheName)
		if os.path.isdir(cachePath):
			for f in os.listdir(cachePath):
				fn = os.path.join(cachePath, f)
				if os.path.isfile(fn):
					os.remove(fn)

			os.rmdir(cachePath)
		time.sleep(0.1)
		os.mkdir(cachePath)

		self._imagePaths = self._collectImages(self._folderPath) # 存储所有图片路径
		self._imageNodes = self._transToImageObjs(self._imagePaths) # 存储所有图片结点
		self._imageSizeStatis = self._calImageSizes(self._imageNodes) # 统计图片的所有size的数量

		for sz, node_list in self._imageSizeStatis.iteritems():
			sx, sy = sz
			cacheImg = Image.new("RGBA", (sx * len(node_list), sy), (255,0,0))
			for idx, node in enumerate(node_list):
				cacheImg.paste(node.obj, (sx*idx, 0))

			cacheName = str(sx)+"_"+str(sy)+".png"
			cacheImg.save(cachePath + "\\" + cacheName)
			#cacheImg.save("_image_joint_cachea.png")

	def _collectImages(self, folderPath):
		if not os.path.isdir(folderPath):
			raise Exception, "invalid folder!"
			return

		images = []

		folders = [folderPath, ]
		while len(folders) > 0:
			cur_folder = folders.pop()

			for iter_folder in os.listdir(cur_folder):
				full_path = os.path.join(cur_folder, iter_folder)

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
			if not p.endswith(".jpg") and not p.endswith(".png"):
				print "process: ", idx / l, p
				continue
			idx += 1
			print "process: ", idx / l, p
			res.append(ImageJointSrcImageNode(p, self._forceSize))
		return res

	def _calImageSizes(self, imageNodes):
		statis = {}

		for node in imageNodes:
			statis.setdefault(node.imgSize, []).append(node)

		return statis

	########################################################################
	###
	########################################################################

	def LoadFromCache(self):
		self._imageNodes = []
		self._imageSizeStatis = {}

		cachePath = os.path.join(self._folderPath, ImageJointLoader._cacheName)
		if not os.path.isdir(cachePath):return

		for cacheImgPath in os.listdir(cachePath):
			try:
				x, y = cacheImgPath.split('.')[0].split('_')
				x = int(x)
				y = int(y)
			except ValueError:
				continue

			img_size_one = IntVec2(x,y)
			img_obj_mul = Image.open(cachePath + "\\" + cacheImgPath)
			x_mul, y_mul = img_obj_mul.size

			for step in range(x_mul/x):
				new_img = Image.new("RGBA", (x, y), (0, 0, 0, 0))
				new_img.paste(img_obj_mul, (x*step, 0))
				self._imageSizeStatis.setdefault(img_size_one, []).append(new_img)
				self._imageNodes.append(ImageJointSrcImageNode.generateByImgObj(new_img, self._forceSize))

		print "LoadFromCache: all: ", len(self._imageNodes)
		for i, j in self._imageSizeStatis.iteritems():
			print "LoadFromCache:", i, len(j)

	########################################################################
	###
	########################################################################

	def GetImageSizeStatis(self):
		res = {}
		for i, j in self._imageSizeStatis.iteritems():
			res[i] = len(j)
		return res

	def GetImageColorStatis(self):
		res = []
		for node in self._imageNodes:
			res.append((node.averageColor, node))
		return res

def main_test():
	loader = ImageJointLoader(r"D:\MyProjects\PythonScript\ImageJoint\test_images")
	# loader.InitCache()
	# time.sleep(2)
	loader.LoadFromCache()

if __name__ == "__main__":
	main_test()