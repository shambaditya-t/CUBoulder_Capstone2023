import cv2
import numpy as np
import pytesseract
import shutil
import os
import random
try:
    from PIL import Image
except ImportError:
    import Image 

#Image Processing
#viasmalltest.jpg
image_name = "viasmalltest.jpg"
image = cv2.imread(image_name)
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("Gray.png",img_gray)
img_blur = cv2.GaussianBlur(img_gray, (3,3) , 0)
#Sobel
sobelx = cv2.Sobel(src=img_blur, ddepth = cv2.CV_64F, dx = 1, dy = 0, ksize=5)
#XAXIS
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
cv2.imwrite("sobel.png", sobelxy)
#Canny
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
cv2.imwrite("Canny.png", edges)

canny_inverse = cv2.bitwise_not(edges)
cv2.imwrite("InverseCanny.png", canny_inverse)
#Circle Detection
circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT,1.5,20,param1=100,param2=100,minRadius=25,maxRadius=68)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    cv2.circle(img_gray,(i[0],i[1]),i[2],(0,0,255),10)
    cv2.circle(img_gray,(i[0],i[1]),2,(0,255,0),10)
cv2.imshow('detected_circles',img_gray)
cv2.waitKey(0)
cv2.imwrite("detected.png", img_gray)

#Pytesseract character detection

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print(pytesseract.image_to_string(Image.open(image_name)))
print(pytesseract.image_to_data(Image.open(image_name)))

#bounding boxes
img = cv2.imread("viasmalltest.jpg")
h, w, c = img.shape
boxes = pytesseract.image_to_boxes(img_gray) 
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
cv2.imshow("bounding box??", img)
cv.waitKey(0)
cv2.destroyAllWindows()


