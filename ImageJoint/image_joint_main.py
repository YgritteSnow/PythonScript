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
	loader = ImageJointLoader(r"J:\PythonScripts\PythonScript\ImageJoint\Camera", (20,20))
	#loader.InitCache()
	#time.sleep(0.4)
	loader.LoadFromCache()
	imgColorList = loader.GetImageColorStatis()
	testImgList = loader.GetImageSizeStatis()
	print "LoadFromCache end"

	print "GenerateSlicer start"
	sizetuple = (3000,3000)
	sliceObj = ImageSlicer(sizetuple)
	sliceObj.GenerateSlicer(testImgList)
	print "GenerateSlicer end"

	print "TestProcessMosaic start"
	mosaicObj = ImageJointMosaic(imgColorList, sliceObj.GetSliceData(), sizetuple, "test.jpg")
	mosaicObj._generateImageFile(mosaicObj._processMosaic())
	print "TestProcessMosaic end"

if __name__ == "__main__":
	main_test()