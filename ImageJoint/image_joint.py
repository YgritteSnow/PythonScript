# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     图片处理框架
# ---------------------------

import os
import pygame todo

MAX_WIDTH = 9999

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

class IntVec2( object ):
    
    def __init__(self, x, y):
        super(self, IntVec2).__init__()
        self._x = x
        self._y = y

    @property
    def x(self):return self._x
    @property
    def y(self):return self._y
    def __hash__(self):return self._x + self._y * MAX_WIDTH
        
class ImageSlicer( object ):
    '''输入图片的大小和书目，得到合适的图片切割方案'''

    def __init__(self, destSize, imagesInfo):
        super(self, ImageSlicer).__init__()
        self._generateSlicer(imagesInfo)

    def _generageSlicer(self, imagesInfo, destSize, error):
        '''递归压栈和回退，得到误差范围内的一个可行的方案：
        @param imageInfo: {图片大小:该大小的数量, }
        @param destSize: 目标大小
        @param error: 为0
        '''
        maxwidth = destSize.x
        
        t_row = [] # [(左下角坐标，宽度), ]
        t_stack = [] # [(开始尝试时的idx，尝试的size, 尝试的idx偏移, 尝试的pos),]
        
        def getNeedWidth(rowlist):
            if len(rowlist) == 0:return 0, maxwidth, 0
            
            last_size, last_width = rowlist[-1]
            nextPosX = last_size.x + last_width
            if nextPosX < maxwidth: return 0, maxwidth - nextPosX, nextPosX
            
            t = MAX_WIDTH
            needWidth = 0
            needPosX = 0
            for quad_size, width in t_row:
                if quad_size.y < t:
                    t = quad_size.y
                    needWidth = width
                    needPosX = quad_size.x
            return minHeight, needWidth, needPosX

        def rowPop(rowlist, popSize, popPos):
            for idx, (pos, width) in enumerate(t_row):
                if pos.x <= popPos:
                    break

            # 如果上边没有命中，那么这里会自然报错
            
        def rowPush(rowlist, pushSize):
            minHeight, needWidth, needPosX = getNeedWidth(rowlist)

            for idx, (pos, width) in enumerate(t_row):
                if pos.x == needPosX:
                    break;
                
            # 如果上边的没有命中，那么这里会自然有一个报错
            if width == pushSize.x:
                newPos = IntVec2(pos.x, pos.y + pushSize.y)
                t_row[idx] = (newPos, width)
            elif width > pushSize.x:
                newPos = IntVec2(pos.x, pos.y + pushSize.y)
                t_row[idx] = (newPos, pushSize.x)
                t_row.insert(idx+1, (IntVec2(pos.x+pushSize.x, pos.y), width - pushSize.x))
            else:
                raise Exception, "width smaller than quad"

            t_idx = idx + 1;
            while t_idx < len(rowlist): # 向后查找能不能合并
                t_pos, t_wid = rowlist[t_idx]
                if newPos.y == t_pos.y:
                    rowlist.pop(t_idx)
                    rowlist[idx][1] += t_wid
                else:
                    break

            t_idx = idx - 1;
            cur_wid = rowlist[idx][1]
            while t_idx >= 0: # 向前查找能不能合并
                t_pos, t_wid = rowlist[t_idx]
                if newPos.y == t_pos.y:
                    rowlist.pop(idx)
                    rowlist[t_idx][1] += cur_wid

                    idx -= 1
                    t_idx -= 1
                    cur_wid = rowlist[idx][1]
                else:
                    break

            return needPosX

        sizes = imagesInfo.keys()
        sizesCount = len(sizes)

        startIdx = random.randint(0, sizesCount)
        currentIdx = 0
        while( True ):
            # 从所有图片中随机选择一个作为下一个起始尝试目标，然后依次遍历所有可尝试的目标，来寻找解决方案
            # 如果没有找到，那么将上一次的选择pop出去，再继续尝试下一个
            
            minHeight, needWidth, t_x = getNeedWidth(t_row)

            # 当最小高度达到所需高度的时候结束
            if minHeight < destSize.y:
                break;
            
            while( currentIdx < sizesCount ):
                imageSize = sizes[(currentIdx + startIdx)%sizesCount]
                if imageSize.x <= needWidth:
                    rowPos = rowPush(t_row)
                    t_stack.append((startIdx, imageSize, currentIdx, rowPos))
                
                    startIdx = random.randint(0, sizesCount)
                    currentIdx = 0

                    break

            if currentIdx == sizesCount:
                if len(t_stack) == 0: # 没有找到解
                    raise Exception, "no solution found"
                
                last_startIdx, last_size, last_sizeIdx, last_pos = t_stack.pop(-1)
                rowPop(t_row, last_size, lastpos)

                currentIdx = last_sizeIdx + 1
                startIdx = last_startIdx

        return t_row
        
        
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
