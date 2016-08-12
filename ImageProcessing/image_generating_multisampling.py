# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图片处理框架
# ---------------------------

import pygame
import random

from image_generating_frame import ImageGeneratingFrame
from lib_math import Vector2

###################################################################
### 随机的点
###################################################################

def random_pixel( image_surface, image_width, image_height ):	
	for x in xrange( image_width ):
		for y in xrange( image_height ):
			image_surface.set_at( (x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) ) )

###################################################################
### 沿着 y 方向模糊
###################################################################

def blur_y( image_surface, image_width, image_height ):
	blur_list = [pygame.Color(0)] * 20
	color_len = 4

	for x in xrange( image_width ):
		for y in xrange( image_height ):
			old_color = image_surface.get_at( (x, y) )

			sum_color = [0] * color_len
			for idx in range(color_len):
				for color in blur_list:
					sum_color[idx] += color[idx]

			sum_color = [d / float(len(blur_list)) for d in sum_color ]

			blur_list.pop()
			blur_list.insert(0, old_color)

			image_surface.set_at( (x, y), sum_color )

###################################################################
### 绘制一条线
###################################################################

def draw_line( image_surface, image_width, image_height, line_start, line_end, color ):
	line_start.sort( line_end )

	step_vec = line_end - line_start
	step_len = step_vec.length()
	step_vec.normalise()

	while step_len >= 0:
		image_surface.set_at( (line_start.x_int + (step_vec*step_len).x_int, line_start.y_int + (step_vec*step_len).y_int), color )
		step_len -= 1

	return

###################################################################
### 过程
###################################################################

tmp = ImageGeneratingFrame( 300, 300, 300, 300 )
for i in range(0, 300, 20):
	tmp.Process(draw_line, Vector2(0, 0), Vector2(i, 299), (255, 255, 255))
tmp.SaveImageToFile()