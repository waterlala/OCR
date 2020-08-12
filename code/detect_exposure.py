import cv2 as cv
import numpy as np
import pandas as pd
from exposure_image import ExposureImage

"""設定計算光影差異量參數"""

# 光影差異量閥值
LD_THRESHOLD = 90
# 設定切割大小
LD_CUT_SIZE = 8
# 腐蝕大小
LD_ERODE_SIZE = 41
# 模糊大小
LD_BLURRY_SIZE = 41
# 模糊係數
LD_BLURRY_SIGMA = 9

"""設定計算文字最低亮度參數"""

# 設定切割大小
WL_CUT_SIZE = 25

# 背景閥值
WL_BACKGROUND_THRESHOLD = 40

# 灰階閥值
WL_GRAY_MAX = 85
WL_GRAY_MIN = 40

# 統一亮度閥值
WL_ALL_BACKGROUND_THRESHOLD = 0.16
WL_ALL_GRAY_THRESHOLD = 0.136

# 401亮度閥值
WL_401_BACKGROUND_THRESHOLD = 0.1696
WL_401_GRAY_THRESHOLD = 0.136

# 403亮度閥值
WL_403_BACKGROUND_THRESHOLD = 0.0464
WL_403_GRAY_THRESHOLD = 0.096

# 資產負債表亮度閥值
WL_BS_BACKGROUND_THRESHOLD = 0.16
WL_BS_GRAY_THRESHOLD = 0.136

# 損益及稅額計算表亮度閥值
WL_IS_BACKGROUND_THRESHOLD = 0
WL_IS_GRAY_THRESHOLD = 0.368


class DetectExposure:

    """
    detect exposure, If image pass, return True, else return False.

    Input：image, type : gray
    
    Ouput：boolean

    Example：

    de = DetectExposure(image)
    if(de.fit() == True):

    """

    def __init__(self, input_image):
        """
        初始化
        """

        """輸入圖片"""
        self.image = input_image

        """光影差異量"""
        self.amount_of_different_light = 0

        """背景占整張圖的比例"""
        self.ratio_of_background_to_image = 0

        """灰階占整張圖的比例"""
        self.ratio_of_gray_to_image = 0

    def fit(self, input_type='None'):
        """
        處理，輸入參數為image的型態，如401, 403, BS(資產負債表), IS(損益及稅額計算表)
        """

        # 取得光影差異量
        self.detect_amount_of_different_light()
        # 取得文字亮度
        self.detect_word_light()
        # 判斷光影差異是否通過
        is_amount_of_different_light = self.judge_amount_of_different_light()
        # 判斷文字亮度是否通過
        is_word_light = self.judge_word_light(input_type)
        # 判斷是否通過
        is_pass = is_amount_of_different_light and is_word_light
        return is_pass

    def fit_401(self):
        """處理401圖片"""
        self.fit('401')

    def fit_403(self):
        """處理403圖片"""
        self.fit('403')

    def fit_BS(self):
        """處理資產負債表圖片"""
        self.fit('BS')

    def fit_IS(self):
        """處理損益及稅額計算表"""
        self.fit('IS')

    def judge_amount_of_different_light(self):
        """判斷光影差異量是否通過"""
        if self.amount_of_different_light >= LD_THRESHOLD:
            return False
        else:
            return True

    def judge_word_light(self, input_type):
        """判斷文字亮度是否通過"""
        if input_type == 'None':
            return self.judge_word_light_threshold(WL_ALL_BACKGROUND_THRESHOLD, WL_ALL_GRAY_THRESHOLD)
        elif input_type == '401':
            return self.judge_word_light_threshold(WL_401_BACKGROUND_THRESHOLD, WL_401_GRAY_THRESHOLD)
        elif input_type == '403':
            return self.judge_word_light_threshold(WL_403_BACKGROUND_THRESHOLD, WL_403_GRAY_THRESHOLD)
        elif input_type == 'BS':
            return self.judge_word_light_threshold(WL_BS_BACKGROUND_THRESHOLD, WL_BS_GRAY_THRESHOLD)
        elif input_type == 'IS':
            return self.judge_word_light_threshold(WL_IS_BACKGROUND_THRESHOLD, WL_IS_GRAY_THRESHOLD)

    def judge_word_light_threshold(self, ratio_of_background_to_image_threshold, ratio_of_gray_to_image_threshold):
        """判斷參數"""
        if self.ratio_of_background_to_image >= ratio_of_background_to_image_threshold and self.ratio_of_gray_to_image >= ratio_of_gray_to_image_threshold:
            return False
        else:
            return True

    def detect_amount_of_different_light(self):
        """偵測光影差異量"""
        # load照片
        image = self.image.copy()
        # 更新圖片型態
        image = self.clear_image_type(image)
        # 腐蝕文字
        image = ~cv.erode(~image, np.ones(
            (LD_ERODE_SIZE, LD_ERODE_SIZE), np.uint8))
        # 模糊圖片
        image = cv.GaussianBlur(
            image, (LD_BLURRY_SIZE, LD_BLURRY_SIZE), LD_BLURRY_SIGMA)
        # 切割圖片
        image_df = self.cut_image(image, LD_CUT_SIZE)
        # 儲存運算值
        value_list = list()
        for single_image in list(image_df['image']):
            value_list.append(single_image.mean())
        self.amount_of_different_light = max(value_list) - min(value_list)

    def detect_word_light(self):
        """偵測文字亮度"""
        # load照片
        image = self.image.copy()
        # 更新圖片型態
        image = self.clear_image_type(image)
        # 光影處理
        ex = ExposureImage(image)
        image = ex.fit()
        # 均值位移
        image = self.mid(image)
        # 更新圖片型態
        image = self.clear_image_type(image)
        # 切割圖片
        image_df = self.cut_image(image, WL_CUT_SIZE)
        # 儲存運算值
        value_list = list()
        # 計算方格最大差值
        for single_image in list(image_df['image']):
            image_max = single_image.max()
            image_min = single_image.min()
            image_dif = image_max - image_min
            value_list.append(image_dif)
        # 統計灰色與背景數量
        for value in value_list:
            if value < WL_BACKGROUND_THRESHOLD:
                self.ratio_of_background_to_image = self.ratio_of_background_to_image + 1
            if value < WL_GRAY_MAX and value >= WL_GRAY_MIN:
                self.ratio_of_gray_to_image = self.ratio_of_gray_to_image + 1
        self.ratio_of_background_to_image = self.ratio_of_background_to_image / len(value_list)
        self.ratio_of_gray_to_image = self.ratio_of_gray_to_image / len(value_list)

    def cut_image(self, input_image, input_range):
        """切割圖片"""
        image_df = pd.DataFrame(
            columns=['image', 'start_x', 'end_x', 'start_y', 'end_y'])
        for i in range(input_range):
            start_x = int(0 + i * (input_image.shape[1] / input_range))
            end_x = int((i+1) * (input_image.shape[1] / input_range))
            for j in range(input_range):
                start_y = int(0 + j * (input_image.shape[0] / input_range))
                end_y = int((j+1) * (input_image.shape[0] / input_range))
                single_image = input_image[start_y:end_y, start_x:end_x]
                image_df.loc[len(image_df)] = [single_image, start_x, end_x, start_y, end_y]
        return image_df

    def clear_image_type(self, input_image):
        "更新圖片型態"
        input_image = np.round(input_image)
        input_image = input_image.astype(np.uint8)
        return input_image

    def mid(self, image):
        "將圖片平均值移動到灰階的中間值 = 256/2"
        image_mean = image.mean()
        image = image - (image_mean - 256/2)
        image[image > 255] = 255
        image[image < 0] = 0
        return image
