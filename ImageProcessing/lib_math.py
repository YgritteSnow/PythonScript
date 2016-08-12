# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图片处理框架
# ---------------------------

import math

class Vector2(object):
	def __init__(self, x, y):
		super(Vector2, self).__init__()
		self._x = x
		self._y = y

	@property
	def x(self):return self._x
	@x.setter
	def x(self, x):self._x = x

	@property
	def y(self):return self._y
	@y.setter
	def y(self, y):self._y = y

	@property
	def x_int(self):return int(round(self._x))
	@property
	def y_int(self):return int(round(self._y))

	def sort( self, vec ):
		self.x, vec.x = min(self.x, vec.x), max(self.x, vec.x)
		self.y, vec.y = min(self.y, vec.y), max(self.y, vec.y)

	def __sub__( self, vec ):return Vector2(self.x - vec.x, self.y - vec.y)
	def __add__( self, vec ):return Vector2(self.x + vec.x, self.y + vec.y)
	def __mul__( self, f ):return Vector2(self.x * f, self.y * f)

	def normalise( self ):
		length = self.length()
		self.x /= length
		self.y /= length

	def length( self ):
		return math.sqrt( self.x * self.x + self.y * self.y )