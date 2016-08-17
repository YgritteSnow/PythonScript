# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图片处理框架
# ---------------------------

import pygame
import random

from image_process_frame import ImageGeneratingFrame
from lib_math import Vector2, LineForGrid, GetLineStepX, GetLineStepY

###################################################################
### 生成：读取贴图
###################################################################

###################################################################
### 生成：随机的点
###################################################################

def random_pixel( image_surface, image_width, image_height ):	
	for x in xrange( image_width ):
		for y in xrange( image_height ):
			image_surface.set_at( (x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) ) )

###################################################################
### 处理：沿着 x 和 y 方向模糊
###################################################################

def blur_y( image_surface, image_width, image_height, buffer_len ):
	blur_list = []
	color_len = 4

	for x in xrange( image_width ):
		for y in xrange( image_height ):
			old_color = image_surface.get_at( (x, y) )
			blur_list.insert(0, old_color)

			sum_color = [0] * color_len
			for idx in range(color_len):
				for color in blur_list:
					sum_color[idx] += color[idx]

			sum_color = [d / float(len(blur_list)) for d in sum_color ]

			if len(blur_list) == buffer_len:
				blur_list.pop()

			image_surface.set_at( (x, y), sum_color )

def blur_x( image_surface, image_width, image_height, buffer_len ):
	blur_list = []
	color_len = 4

	for y in xrange( image_width ):
		for x in xrange( image_height ):
			old_color = image_surface.get_at( (x, y) )
			blur_list.insert(0, old_color)

			sum_color = [0] * color_len
			for idx in range(color_len):
				for color in blur_list:
					sum_color[idx] += color[idx]

			sum_color = [d / float(len(blur_list)) for d in sum_color ]

			if len(blur_list) == buffer_len:
				blur_list.pop()

			image_surface.set_at( (x, y), sum_color )

###################################################################
### 处理：某个特定方向模糊
###################################################################

def blur_line( image_surface, image_width, image_height, buffer_len, blur_direct, start_point ):
	'''
	沿着一条线模糊
	'''
	if blur_direct.is_trivial():return

	blur_line = LineForGrid( start_point, blur_direct )

	blur_list = []
	color_len = 4
	for point in blur_line.YieldXY( max_x = image_width, max_y = image_height ):
		old_color = image_surface.get_at( (point.x_int, point.y_int) )
		blur_list.insert(0, old_color)

		sum_color = [0] * color_len
		for idx in range(color_len):
			for color in blur_list:
				sum_color[idx] += color[idx]

		sum_color = [d / float(len(blur_list)) for d in sum_color ]

		if len(blur_list) == buffer_len:
			blur_list.pop()

		image_surface.set_at( (point.x_int, point.y_int), sum_color )

def blur_vec( image_surface, image_width, image_height, buffer_len, blur_direct ):
	'''
	遍历面上的每一条线，对其进行模糊
	'''
	start_x = 0
	start_y = GetLineStepY( blur_direct )

	for step_x in range( start_x, image_width, abs(GetLineStepX( blur_direct )) ):
		blur_line( image_surface, image_width, image_height, buffer_len, blur_direct, Vector2(step_x, start_y) )

	for step_y in range( start_y, image_height, abs(GetLineStepY( blur_direct )) ):
		blur_line( image_surface, image_width, image_height, buffer_len, blur_direct, Vector2(start_x, step_y) )

###################################################################
### 处理：绘制一条线
###################################################################

def draw_line_1( image_surface, image_width, image_height, line_start, line_end, color ):
	line_start.sort( line_end )

	step_vec = line_end - line_start
	step_len = step_vec.length()
	step_vec.normalise()

	while step_len >= 0:
		image_surface.set_at( (line_start.x_int + (step_vec*step_len).x_int, line_start.y_int + (step_vec*step_len).y_int), color )
		step_len -= 1

	return

def draw_line( image_surface, image_width, image_height, line_start, line_end, color ):
	cur_line = LineForGrid( line_start, endPoint = line_end )
	for point in cur_line.YieldXY( max_x = image_width, max_y = image_height ):
		image_surface.set_at( (point.x_int, point.y_int), color )

###################################################################
### 主流程
###################################################################

tmp = ImageGeneratingFrame( 300, 300, 300, 300 )
for i in range(0, 300, 20):
	tmp.Process(draw_line, Vector2(0, 0), Vector2(i, 299), (255, 255, 255))
#tmp.Process(random_pixel)
#tmp.Process(blur_vec, 20, Vector2(2,1) )
tmp.SaveImageToFile()