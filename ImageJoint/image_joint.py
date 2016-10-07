# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图片处理框架
# ---------------------------

import os
import pygame

class ImageNode( object ):
    '''单个图片'''

    def __init__(self, imagePath):
        super(self, ImageNode).__init__()
        self._imageData = None # todo 用pygame加载图片
        self._queryData(imagePath)

    def _queryData(self, imagePath):
        self._surface = None # todo 用pygame加载图片
        self._luminance = 1 # todo

    def GetSortKey(self):
        return 1 # todo

        
class ImageLoader( object ):
    '''加载多个图片'''
    
    def __init__(self, sourcePath):
        super(self, ImageLoader).__init__()
        self._imageList = []
        self._queryImages(sourcePath)

    def _queryImages(self, sourcePath):
        self._imageList = []
        for dirname in os.listdir(sourcePath):
            if os.path.isdir(a):continue
            if not dirname.endswith(".jpg"):continue
            self._imageList.append(ImageNode(sourcePath + '\\' + a));

        return

    
    def _sortImages(self):
        self._imageList.sort(key=lambda x:x.GetSortKey())

        return

    def FindImage(self):pass
        
class ImagePattern( object ):
    '''源图片及其处理'''
    
    def __init__(self, patternImage):
        super(self, ImagePattern).__init__()

    def Slice(self, slicer):pass

    def SortPattern(self):pass

    def GetPattern(self):pass

    def SaveNewImage(self):pass

patternPath = ''
pattern = ImagePattern(patternPath)

slicer = ImageSlicer()
pattern.Slice(slicer)

sourcePath = ''
sourceImages = ImageLoader(sourcePath)

destFilePath = ''
matcher = ImageMatcher()
matcher.SaveImage(pattern, sourceImages, destFilePath)
