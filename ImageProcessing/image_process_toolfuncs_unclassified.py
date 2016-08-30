# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     未分类的一些处理函数
# ---------------------------

import pygame
import random
import math

from lib_math import Vector2, LineForGrid

###################################################################
### 生成：读取贴图
###################################################################

def load_image( image_surface, image_width, image_height, src_filename ):
	src_surface = pygame.image.load(src_filename)
	#src_surface.convert
	image_surface.blit( src_surface, (0, 0) )

###################################################################
### 生成：随机的点
###################################################################

def random_pixel( image_surface, image_width, image_height ):	
	for x in xrange( image_width ):
		for y in xrange( image_height ):
			image_surface.set_at( (x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) ) )

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
### 处理：试试随便一个处理函数迭代迭代有什么效果
###################################################################

def magicFunc( vec, max_x, max_y ):
	old_x, old_y = vec.x / max_x, vec.y / max_y
	vec.x = min( 1, (old_x + old_y + random.random()/111 )/2 ) * max_x
	vec.y = min( 1, math.sqrt(old_x * old_y) + random.random()/111 ) * max_y

def magicProcess( image_surface, image_width, image_height ):
	origin_point = Vector2( 1, image_height-1 )
	count = 10
	while count > 0:
		count -= 1
		old_color = image_surface.get_at( (origin_point.x_int, origin_point.y_int) )
		image_surface.set_at( (origin_point.x_int, origin_point.y_int), old_color + pygame.Color(100, 0, 0, 0) )
		magicFunc( origin_point, image_width-1, image_height-1 )
		print origin_point
