'''
Image Processing
Last Updated: 11/8/2022
'''

import cv2
import numpy as np
import pytesseract
import shutil
import os
import random
import time
import math

try:
    from PIL import Image
except ImportError:
    import Image


def apply_gray(image_name,path):
    full_path = path + '\\'
    full_path += image_name
    image = cv2.imread(full_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def apply_Gaussian(image):
    gaussian_image = cv2.GaussianBlur(image, (3,3), 0)
    return gaussian_image

def apply_sobels(image):
    sobelxy = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
    return sobelxy

def apply_canny(image):
    canny_image = cv2.Canny(image=image, threshold1=100, threshold2=200)
    return canny_image

def inverse(image):
    inverse_image = cv2.bitwise_not(edges)

def apply_via_detection(image_name,image,par1,par2,min_Rad, max_Rad):
    #Cannot simply use the image for houghcircles
    #Need to convert to unit8
    #norm_image = cv2.normalize(src=image, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    #or not?
    circ_array = np.array([0,0], dtype = object)
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1.5,20,param1=min_Rad,
                               param2=max_Rad,minRadius=0,maxRadius=20)
    #print(circles)
    try:
        circles = np.uint16(np.around(circles))
        
        for i in circles[0,:]:
            #cv2.circle(image,center_coordinates,radius,color,thickness)
            circle = [i[0],i[1]]
            circ_array = np.append(circ_array, circle)
            #print([i[0],i[1]])
            cv2.circle(image,(i[0],i[1]),i[2],(0,0,255),10)
            cv2.circle(image,(i[0],i[1]),2,(0,255,0),10)
        #print(circ_array)
        new_shape = len(circ_array)/2
        new_shape = math.floor(new_shape)
        print(new_shape)
        circ_array = np.reshape(circ_array,[new_shape,2])
        print(circ_array)
        np.savetxt(image_name[:-4] + ".csv", circ_array, delimiter=',')
        return image
    except Exception as e:
        print(e)
        print("Error: No Via Holes Detected")
        return image

def detect_text(image_name):
    print(pytesseract.image_to_string(Image.open(image_name)))
    print(pytesseract.image_to_data(Image.open(image_name)))


def draw_bounding(image_name,path):
    #bounding boxes
    full_path = path + '\\'
    full_path += image_name
    img = cv2.imread(full_path)
    
    h, w, c = img.shape

    #argument was img_gray
    boxes = pytesseract.image_to_boxes(img) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    cv2.imwrite(os.path.join(os.getcwd()+"\\output" , "bounding_" + image_name),img)
    #cv2.imshow("bounding box??", img)
    #cv2.waitKey(0)

def run_process(image_name, path,minrad,maxrad):
    print("Testing: " + image_name)
    image = apply_gray(image_name,path)
    #original: 100, 100, 25, 68,
    new_image = apply_via_detection(image_name,image,100,100, minrad, maxrad)
    cv2.imwrite(os.path.join(os.getcwd()+"\\output" , image_name),new_image)
    '''
    try:
        draw_bounding(image_name,path)
    except:
        print("NoneType Error")
    '''
    #cv2.imshow("Detected Vias", new_image)
    #cv2.waitKey(0)
   
    
    

def run(image_list,directory, minrad, maxrad):
    path = os.getcwd()
    full_path = path + directory
    print("PATH: " + full_path)
    
    for image in image_list:
        run_process(image, full_path,minrad,maxrad)
    cv2.destroyAllWindows()
