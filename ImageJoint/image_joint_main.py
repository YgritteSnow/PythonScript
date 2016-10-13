# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     总的处理函数
# ---------------------------

from image_joint_mosaic import *
from image_joint_slice import *
from image_joint_imgloader import *

def main_test():
	print "LoadFromCache start"
	loader = ImageJointLoader(r"D:\MyProjects\PythonScript\ImageJoint\test_images\Camera", (10,10))
	#loader.InitCache()
	#time.sleep(0.4)
	loader.LoadFromCache()
	imgColorList = loader.GetImageColorStatis()
	for c,i in imgColorList:
		print "color: ", c
	testImgList = loader.GetImageSizeStatis()
	print "LoadFromCache end"

	print "GenerateSlicer start"
	sizetuple = (400, 400)
	sliceObj = ImageSlicer(sizetuple)
	sliceObj.GenerateSlicer(testImgList)
	print "GenerateSlicer end"

	print "TestProcessMosaic start"
	mosaicObj = ImageJointMosaic(imgColorList[:100], sliceObj.GetSliceData(), sizetuple, "test.jpg")
	mosaicObj._generateImageFile(mosaicObj._processMosaic())
	print "TestProcessMosaic end"

if __name__ == "__main__":
	main_test()