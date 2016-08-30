# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图片处理框架
# ---------------------------

import math
import random

###################################################################
### 二维向量
###################################################################

class Vector2( object ):
	def __init__( self, x, y ):
		super( Vector2, self ).__init__()
		self._x = float(x)
		self._y = float(y)

	@property
	def x( self ):return self._x
	@x.setter
	def x( self, x ):self._x = x

	@property
	def y( self ):return self._y
	@y.setter
	def y( self, y ):self._y = y

	@property
	def x_int( self ):return int( round( self._x ) )
	@property
	def y_int( self ):return int( round( self._y ) )

	def GetGrid( self ):return Vector2( self.x_int, self.y_int )

	def sort( self, vec ):
		self.x, vec.x = min( self.x, vec.x ), max( self.x, vec.x )
		self.y, vec.y = min( self.y, vec.y ), max( self.y, vec.y )

	def __sub__( self, vec ):return Vector2( self.x - vec.x, self.y - vec.y )
	def __add__( self, vec ):return Vector2( self.x + vec.x, self.y + vec.y )
	def __mul__( self, f ):return Vector2( self.x * f, self.y * f )
	def __div__( self, vec_or_f ):
		if isinstance( vec_or_f, Vector2 ):
			x_div = (self.x / vec_or_f.x) if vec_or_f.x > vec_or_f.y else (self.y / vec_or_f.y)
		else:
			return Vector2( self.x / vec_or_f, self.y / vec_or_f )

	def __str__( self ):return "<Vector2>(%.2f, %.2f)" % (self.x, self.y, )

	def normalise( self ):
		length = self.length()
		if not length:return
		self.x /= length
		self.y /= length

	def length( self ):
		return math.sqrt( self.x * self.x + self.y * self.y )

	def is_trivial( self ):
		return self.length() == 0

###################################################################
### 射线 / 线段
###################################################################

class Line( object ):

	def __init__( self, startPoint, lineDirect = None, endPoint = None ):
		super( Line, self ).__init__()

		if lineDirect is not None:
			self.lineDirect = lineDirect
		elif endPoint is not None:
			self.lineDirect = endPoint - startPoint
		else:
			assert 0

		self.lineDirect.normalise()
		self.startPoint = startPoint

	def __str__( self ):return "<line>(startPoint:(%.2f, %.2f), direct:(%.2f, %.2f))" % (self.startPoint.x, self.startPoint.y, self.lineDirect.x, self.lineDirect.y, )

	def GetYByX( self, x ):
		if self.lineDirect.x == 0:return 0
		return ( x - self.startPoint.x ) / self.lineDirect.x * self.lineDirect.y + self.startPoint.y

	def GetXByY( self, y ):
		if self.lineDirect.y == 0:return 0
		return ( y - self.startPoint.y ) / self.lineDirect.y * self.lineDirect.x + self.startPoint.x

###################################################################
### 适用于格子的线段
###################################################################

class LineForGrid( Line ):

	def __init__( self, startPoint, lineDirect = None, endPoint = None ):
		super( LineForGrid, self ).__init__(startPoint, lineDirect = lineDirect, endPoint = endPoint)

		if abs(self.lineDirect.x) > abs(self.lineDirect.y):
			self.step = Vector2(1, self.lineDirect.y / self.lineDirect.x) #沿着x方向步进
		else:
			self.step = Vector2(self.lineDirect.x / self.lineDirect.y, 1) #沿着y方向步进

	def YieldXY( self, max_x = None, max_y = None ):
		'''
		遍历每一个经过的格子，endPointMax代表可能到达的最远点
		这里的max_x和max_y选取的是距离射线正向最近的点，不包括反向
		'''
		maxStepCount_x = 999999
		maxStepCount_y = 999999
		if max_x is not None and self.step.x != 0:
			maxStepCount_x = (max_x - 1 - self.startPoint.x) / self.step.x
		if max_y is not None and self.step.y != 0:
			maxStepCount_y = (max_y - 1 - self.startPoint.y) / self.step.y

		maxStepCount = maxStepCount_x if maxStepCount_x < maxStepCount_y else maxStepCount_y

		for stepCount in range( int(round(maxStepCount, 0 )) ):
			yield self.startPoint + self.step * stepCount

	def GetXStep( self ):return self.step.x
	def GetYStep( self ):return self.step.y

###################################################################
### 给定一个直线的方向，分别使用x和y方向的步进，来使这个直线划过平面上所有的点
### 此函数输出的是这个步进的大小
###################################################################

def GetLineStepX( line_direct ):
	if line_direct.y == 0:
		return None
	elif abs(line_direct.x) > abs(line_direct.y):
		return int(line_direct.x / line_direct.y)
	else:
		return 1

def GetLineStepY( line_direct ):
	if line_direct.x == 0:
		return None
	elif abs(line_direct.y) > abs(line_direct.x):
		return int(line_direct.y / line_direct.x)
	else:
		return 1
