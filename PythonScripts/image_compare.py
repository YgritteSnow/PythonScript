# -*- code - utf-8 -*-

import pygame

EPSILON = 2

def IsImageSame_strict(image1, image2):
	sur1 = pygame.image.load(image1)
	sur2 = pygame.image.load(image2)
	if sur1.get_size() != sur2.get_size():
		return False

	for x in range(sur1.get_size()):
		for y in range(sur2.get_size()):
			if sur1.get_at((x,y)) - sur2.get_at((x,y)) > EPSILON:
				return False
	
	return True

def 
