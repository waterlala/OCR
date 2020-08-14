import cv2 as cv
import numpy as np
import pandas as pd
"""光影處理參數"""

#腐蝕大小
ERODE_SIZE = 21
#中值模糊參數
MEDIANBLUR_PARAMETER = 21
#高斯模糊大小
BLURRY_SIZE = 21
#高斯模糊係數
BLURRY_SIGMA = 9


class CorrectExposure:
    def __init__(self, input_image):
        """初始化"""

        #輸入圖片
        self.image = input_image

    def fit(self):
        """處理"""

        #load照片
        image = self.image.copy()
        #更新圖片型態
        image = self.clear_image_type(image)
        #設定差值圖片
        df_image = image.copy()
        #腐蝕文字
        df_image = ~cv.erode(~df_image, np.ones((ERODE_SIZE, ERODE_SIZE), np.uint8))
        #中值模糊
        df_image = cv.medianBlur(df_image, MEDIANBLUR_PARAMETER)
        #高斯模糊
        df_image = cv.GaussianBlur(df_image, (BLURRY_SIZE, BLURRY_SIZE), BLURRY_SIGMA)
        #差值處理
        image = 255 - cv.absdiff(image, df_image)
        #更新圖片型態
        image = self.clear_image_type(image)
        #均值位移
        image = self.mid(image)
        #更新圖片型態
        image = self.clear_image_type(image)
        return image

    def clear_image_type(self, input_image):
        """更新圖片型態"""
        
        input_image = np.round(input_image)
        input_image = input_image.astype(np.uint8)
        return input_image

    def mid(self, image):
        """將圖片平均值移動到灰階的中間值 = 256/2"""

        image_mean = image.mean()
        image = image - (image_mean - 256 / 2)
        image[image > 255] = 255
        image[image < 0] = 0
        return image