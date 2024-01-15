import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt
import imutils
path = os.getcwd() + "\Images_Pattern"
images = os.listdir(path)

for image in images:
    image_path = 'Images_Pattern/' + image
    #Read in Image and Template 
    img_rgb = cv.imread(image_path)
    #img_rgb = imutils.rotate(img_rgb,90)
    template = cv.imread('template.jpg',0)
    #Convert Image to Gray Scale
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    
    width, height = template.shape[::-1] #Reverse BGR to RGB? 

    result = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    output_path = 'Output/' + image
    #cv.imwrite(output_path, result * 255)

    threshold = 0.8
    location = np.where(result >= threshold)
    print(image)
    for point in zip(*location[::1]):
        #weird issue with point?
        print(point)
        cv.rectangle(img_rgb, point, (point[0] + width, point[1] + height), (0,0,255), 2)
    cv.imwrite(output_path, img_rgb)
