# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图片处理框架
# ---------------------------

import pygame

class ImageGeneratingFrame( object ):

	def __init__(self, screen_width, screen_height, image_width, image_height ):
		super(ImageGeneratingFrame, self).__init__()

		self.m_screen_width = screen_width
		self.m_screen_height = screen_height
		self.m_image_width = image_width
		self.m_image_height = image_height

		self.m_screen = pygame.display.set_mode((self.m_screen_width, self.m_screen_height))
		self.m_img_surface = pygame.Surface((self.m_image_width, self.m_image_height))

	def Process( self, func, *arg, **kwargs):
		func(self.m_img_surface, self.m_image_width, self.m_image_height, *arg, **kwargs)

		return

	def ShowImageOnScreen( self ):
		
		return

	def SaveImageToFile( self, filename ):
		pygame.image.save(self.m_img_surface, filename)

		return
