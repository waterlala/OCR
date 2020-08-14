import cv2
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

class OCRTool:
    def __init__(self):
        pass
    
    def show_hist(self, img):
        plt.hist(img.ravel(), bins = 50)
        plt.show()
    
    def show_image(self, img):
        plt.figure(figsize = (10, 10), dpi=200)
        plt.imshow(img, cmap ='gray')
    
    def compare(self, img, a):
        img = img * float(a)
        img[img > 255] = 255
        img = np.round(img)
        img = img.astype(np.uint8)
        return img
    
    def binarization(self, img):
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)
        return img
    
    def equil_hist(self, img):
        img = cv2.equalizeHist(img)
        return img
    
    def gamma_trans(self, img, gamma):
        gamma_table = [np.power(x/255.0,gamma)*255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(img,gamma_table)
    
    def mid(self, img):
        img_mean = img.mean()
        img = img - (img_mean - 256/2)
        img[img > 255] = 255
        img[img < 0] = 0
        return img
        
    def clear_img_type(self, img):
        img = np.round(img)
        img = img.astype(np.uint8)
        return img
    
    def show_min_different(self, img):
        img = self.clear_img_type(img)
        bg_img = cv2.dilate(img, np.ones((41,41), np.uint8))
        kernel_size = (41, 41);
        sigma = 9
        bg_img = cv2.GaussianBlur(bg_img, kernel_size, sigma)

        dif = list()
        r = 13
        for i in range(r):
            start_x = int(0 + i *(img.shape[1] / r))
            end_x = int((i+1) * (img.shape[1] / r))
            for j in range(r):
                start_y = int(0 + j * (img.shape[0] / r))
                end_y = int((j+1) * (img.shape[0] / r))
                s_img = bg_img[start_y:end_y,start_x:end_x]
                dif.append(s_img.mean())
        return pd.Series(dif).max() - pd.Series(dif).min()