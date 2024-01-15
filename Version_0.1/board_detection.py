import cv2
import numpy as np


image = cv2.imread('colortest6.jpg')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(gray,(5,5),0)
ret3,th3 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite("Threshold3.jpg",th3)
#Thresholding on the grayscale image
#Creating binary image 
ret,threshold = cv2.threshold(gray, 127, 255, 0)
cv2.imwrite("threshold.jpg",threshold)

threshold2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                      cv2.THRESH_BINARY,11,2)
cv2.imwrite("threshold2.jpg",threshold2)
#cv2.imshow("threshold",threshold)
#cv2.waitKey(0)

#Find contours
contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contour_image = cv2.drawContours(image, contours, 3, (0,255, 255), 3)
cv2.imwrite("contours.jpg",contour_image)
num_contours = len(contours)
print("Detect: " + str(num_contours) + " contours")
i = 0
for contour in contours:
    i += 1;
    #print("Contour:" + str(i))
    x1, y1 = contour[0][0]
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour,True), True)

    if(len(approx) == 4):
        x, y, w, h = cv2.boundingRect(contour)
        ratio = float(w)/h

        if(ratio >= 0.9 and ratio <= 1.1):
            image = cv2.drawContours(image, [contour], -1, (0,255, 255), 3)
            #cv2.putText(image, "Square", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        else:
            #cv2.putText(image, "Rectangle", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            image = cv2.drawContours(image,[contour], -1, (0,255,0),3)
cv2.imwrite('test.jpg',image)
#cv2.imshow("Shapes", image)
#cv2.waitKey(0)
cv2.destroyAllWindows()
