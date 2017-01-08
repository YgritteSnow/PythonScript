# -*- coding: utf-8 -*- 

###################################################
### 检测某个文件夹中所有与其他类似的资源
###################################################

import os.path

Enum_Parser_Image = 1 # 按照图片进行解析和对比
Enum_Parser_file = 2 # 按照文本文件进行解析和对比

g_resource_postfix = {
	(".png", ".jpg", ".bmp", ):Enum_Parser_Image,
	(".plist", ):Enum_Parser_file,
	(".csd", ):Enum_Parser_file,
}

