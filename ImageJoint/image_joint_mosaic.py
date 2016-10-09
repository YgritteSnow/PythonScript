# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     将给定的像素尽力拼合成给定的图形
# ---------------------------

import os
import pygame

class ImageJointMosaic( object ):
    '''
    计算出一个良好的方案，将给定的若干张图片放入切分好了的目标图片中，尽可能的模拟目标图片的效果
    '''

    def __init__(self, destImage, sliceData, srcImageList):
        super(ImageJointMosaic, self).__init__()

        self._destImage = destImage
        self._sliceData = sliceData
        self._srcImageList = srcImageList

    def _processMosaic(self, destMosaic, srcImageList):
        '''
        主计算函数
        @param destMosaic: 目标图片，格式为：[(切块左上角pos，切块size，切块原color)]
        @param srcImageList: 源图片，格式为：[imageInfo, ]
        '''
        result = []

        last_color_surplus = 0 # 上一次模拟时的颜色的剩余（已经乘以了面积）
        for slice_pos, slice_size, slice_color in destMosaic:
            cur_dest_color = last_color_surplus / slice_size.Area() + slice_color
            find_src_img = self.FindSlice(cur_dest_color)
            result.append( find_src_img )
            last_color_surplus = ( cur_dest_color - find_src_img.Color() ) * find_src_img.Area()

        return result

    def ProcessMosaic(self):
        