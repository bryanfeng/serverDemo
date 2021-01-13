# -*- coding:utf-8 -*-
from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse

import random as rng

rng.seed(12345)

# 是否输出中间图像
detail_image = True

# 要检测的区域，占整张图的占比阀值

# 空白占当前区域的预警阀值



def saveDetailImage(name, img):
    if detail_image:
        cv.imwrite(name, img)



def thresh_callback(val, gray, src):
    threshold = val
    src_gray = gray
    src = src
    
    # 边缘检测，轮廓
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    
    
    contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)

    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
    
    
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    
    for i in range(len(contours)):

        color = (255, 255, 255)
        cv.drawContours(drawing, contours_poly, i, color)

        # 0 1 2 3 左顶宽高
        xLeft = int(boundRect[i][0])
        wight = int(boundRect[i][2])
        xRight = int(boundRect[i][0]+boundRect[i][2])

        yTop = int(boundRect[i][1])
        hight = int(boundRect[i][3])
        yBottom = int(boundRect[i][1]+boundRect[i][3])
        

        # TODO 这里改为占比
        area = wight*hight
        if area < 600 or wight< 50 or hight< 50 :
            continue
        #print ("area : ", area, "wight:", wight, "hight:", hight )
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        
        cv.rectangle(drawing, (xLeft, yTop),(xRight, yBottom), color, 2)

        # y顶、y底、x左、x右 （非宽高）
        cutres = src_gray[yTop:yBottom, xLeft:xRight]
        
        hist = cv.calcHist([cutres], [0], None, [2], [0, 256])
        num_black = hist[0][0]
        num_white = hist[1][0]
        black_precent = num_black / (num_black + num_white)
        #print ("black_precent: " ,black_precent)
        if black_precent > 0.85:
            #print ("hist: " , hist,"num_black : ", num_black, "num_white:", num_white, "black_precent:", black_precent )

            cv.rectangle(src, (xLeft, yTop),(xRight, yBottom), color, 2)


            pass
        
    saveDetailImage("7_rectangle.jpg", drawing)
    saveDetailImage("9_finish.jpg", src)

    #cv.imshow('drawing', drawing)
    #cv.imshow('Contours', src)


parser = argparse.ArgumentParser(description='Code for Creating Bounding boxes and circles for contours tutorial.')
parser.add_argument('--input', help='Path to input image.', default='./sample5.png')
args = parser.parse_args()
src = cv.imread(args.input)
if src is None:
    print('Could not open or find the image:', args.input)
    exit(0)







# 1.png
# Convert image to gray and blur it
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
saveDetailImage('1_src_gray.jpg', src_gray)


# 2.png
gradX = cv.Sobel(src_gray, ddepth=cv.CV_32F, dx=1, dy=0, ksize=-1)
gradY = cv.Sobel(src_gray, ddepth=cv.CV_32F, dx=0, dy=1, ksize=-1)
# subtract the y-gradient from the x-gradient
gradient_src = cv.subtract(gradX, gradY) 
saveDetailImage('2_sobel.jpg', gradient_src)


# 3.png
gradient = cv.convertScaleAbs(gradient_src)
saveDetailImage('3_convertScaleAb_sobel.jpg', gradient)

# 4.png
resp = None
(_, thresh) = cv.threshold(gradient, 0, 255, cv.THRESH_BINARY)
saveDetailImage('4_threshold.jpg', thresh)


# 5.png
morph_size = 2
morph_elem = cv.MORPH_RECT
element = cv.getStructuringElement(morph_elem, (2*morph_size + 1, 2*morph_size+1), (morph_size, morph_size))
dst = cv.morphologyEx(thresh, cv.MORPH_CLOSE, element)
saveDetailImage('5_morphology.jpg', dst)


# 6.png

# 边缘检测，轮廓
threshold = 255
canny_output = cv.Canny(dst, threshold, threshold * 2)
contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
saveDetailImage('6_canny.jpg', canny_output)

# 7.png
thresh_callback(255, dst, src)



#hist = cv.calcHist([thresh], [0], None, [2], [0, 2])
#num_black = hist[0][0]
#num_white = hist[1][0]

#is_empty = num_white / num_black 

#print ("is_empty" + str(is_empty))
#cv.imshow('source_window', dst)
#max_thresh = 255
#thresh = 100 # initial threshold#
#cv.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, thresh_callback)
#thresh_callback(thresh)
#cv.imshow('source_window', canny_output)
#cv.waitKey()


#
#
