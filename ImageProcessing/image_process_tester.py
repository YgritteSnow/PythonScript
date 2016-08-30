# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图片处理框架
# ---------------------------

from image_process_frame import ImageGeneratingFrame

from image_process_toolfuncs_unclassified import *
from image_process_toolfuncs_blur import *

###################################################################
### 主流程
###################################################################

tmp = ImageGeneratingFrame( 300, 300, 300, 300 )
#tmp.Process(load_image, "sample.bmp")
#for i in range(0, 300, 20):
#	tmp.Process(draw_line, Vector2(0, 0), Vector2(i, 299), (255, 255, 255))
#tmp.Process(random_pixel)
#tmp.Process(blur_vec, 20, Vector2(2,1) )
tmp.Process(magicProcess)
tmp.SaveImageToFile("img_surface.bmp")