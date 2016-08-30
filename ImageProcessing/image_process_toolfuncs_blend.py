# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图像混合，参考Photoshop说明文档
#     https://helpx.adobe.com/cn/photoshop/using/blending-modes.html
#
#     给定两张图片，然后使用不同的模式进行混合。
# ---------------------------

import pygame
import random
import math

from lib_math import Vector2, LineForGrid, GetLineStepX, GetLineStepY

Enum_Blend_Normal 		= 1 	#正常模式
Enum_Blend_Dissolve 	= 2 	#溶解
Enum_Blend_Behind 		= 3 	#背后
Enum_Blend_Clear 		= 4 	#清除
Enum_Blend_Darken 		= 5 	#变暗
Enum_Blend_Multiply 	= 6 	#正片叠底
Enum_Blend_ColorBurn 	= 7 	#颜色加深
Enum_Blend_LinearButn 	= 8 	#线性加深
Enum_Blend_Lighten 		= 9 	#变亮
Enum_Blend_Screen 		= 10 	#滤色
Enum_Blend_ColorDodge 	= 11 	#颜色减淡
Enum_Blend_LinearDodge 	= 12 	#线性减淡（添加）

###################################################################
### 混合函数
###################################################################

def _blend_frame( image_surface_dst, image_width_dst, image_height_dst, 
	image_surface_src, image_width_src, image_height_src, 
	image_pos_src, 
	blend_mode, 
	*arg, **kwargs):
	'''
	框架函数，整合几个函数中的相同的代码
	'''
	mode_map = {
		Enum_Blend_Normal: 		_blend_normal, 
		Enum_Blend_Dissolve: 	_blend_dissolve, 
		Enum_Blend_Behind: 		_blend_behind, 
		Enum_Blend_Clear: 		_blend_clear, 
	}

	func = mode_map.get(blend_mode)
	if func is None:return

	for x in xrange( image_width_src ):
		real_x = image_pos_src.x_int + x
		if real_x >= image_width_dst:
			break;

		for y in xrange( image_height_src ):
			real_y = image_pos_src.y_int + y
			if real_y >= image_height_dst:
				break

			src_color = image_surface_src.get_at( (x, y) )
			dst_color = image_surface_dst.get_at( (x, y) )
			image_surface_dst.set_at( (real_x, real_y), func(dst_color, src_color) )

	return

def _blend_normal( dst_color, src_color ):
	'''
	正常
	编辑或绘制每个像素，使其成为结果色。
	'''
	src_alpha = src_color.a / 256.0
	return src_color * src_alpha + dst_color * (1-src_alpha)

def _blend_dissolve( dst_color, src_color ):
	'''
	溶解
	根据任何像素位置的不透明度，结果色由基色或混合色的像素随机替换。
	'''
	src_alpha = src_color.a / 256.0
	return src_color if random.random() < src_alpha else dst_color

def _blend_behind( dst_color, src_color ):
	'''
	背后
	仅在图层的透明部分编辑或绘画。
	'''
	return _blend_normal(src_color, dst_color)

def _blend_clear( dst_color, src_color ):
	'''
	清除
	编辑或绘制每个像素，使其透明。
	'''
	return pygame.Color()

def _blend_darken( dst_color, src_color ):
	'''
	变暗
	查看每个通道中的颜色信息，并选择基色或混合色中较暗的颜色作为结果色。
	'''
	return pygame.Color(min(dst_color.r, src_color.r), 
		min(dst_color.g, src_color.g), 
		min(dst_color.b, src_color.b), 
		min(dst_color.a, src_color.a) )

def _blend_multiply( dst_color, src_color ):
	'''
	正片叠底
	查看每个通道中的颜色信息，并将基色与混合色进行正片叠底（multiply）。
	'''
	return pygame.Color(dst_color.r * src_color.r / 256, 
		dst_color.g * src_color.g / 256, 
		dst_color.b * src_color.b / 256, 
		dst_color.a * src_color.a / 256, 
		)

###################################################################
### 框架函数
###################################################################

def blend( image_surface_dst, image_width_dst, image_height_dst, 
	image_surface_src, image_width_src, image_height_src, 
	image_pos_src, 
	blend_mode, 
	*arg, **kwargs):
	_blend_frame(image_surface_src, image_width_src, image_height_src, 
		image_surface_dst, image_width_dst, image_height_dst, 
		image_pos_src, 
		*arg, **kwargs)
