import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy import ndimage

image1 = 'images3/test2_1.jpg'
image2 = 'images3/test2_2.jpg'

input_images_path = [image1, image2]

def calculate_matches(des1, des2):

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test - LOWE
    result = []
    for m, n in matches:
        if (m.distance / n.distance) < 0.8:
            result.append(m)

    return result


images = []
kp = []
desc = []

for img in input_images_path:
    image = cv2.imread(img)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    sift = cv2.xfeatures2d.SIFT_create()

    k, des = sift.detectAndCompute(image,None)

    images.append(image)
    kp.append(k)
    desc.append(des)

matches1 = calculate_matches(desc[0],desc[1])
src_pts12 = np.float32([kp[0][m.queryIdx].pt for m in matches1]).reshape(-1, 1, 2)
dst_pts12 = np.float32([kp[1][m.trainIdx].pt for m in matches1]).reshape(-1, 1, 2)
H12, _ = cv2.findHomography(src_pts12, dst_pts12, cv2.RANSAC)

h1,w1 = images[0].shape[:2]
h2,w2 = images[1].shape[:2]

pts1 = np.float32([[0,0],[0,h1],[w1,h1],[w1,0] ]).reshape(-1,1,2)
dst1 = cv2.perspectiveTransform(pts1, H12)

pts2 = np.float32([[0,0],[0,h2],[w2,h2],[w2,0] ]).reshape(-1,1,2)
dst2 = cv2.perspectiveTransform(pts2, inv(H12))

x_min = 1000
y_min = 1000
x_max = 0
y_max = 0

for i in range(4):
    x = dst1[i][0][0]
    y = dst1[i][0][1]
    if x > x_max:
        x_max = x
    if x < x_min:
        x_min = x
    if y > y_max:
        y_max = y
    if y < y_min:
        y_min = y
        
for i in range(4):
    x = dst2[i][0][0]
    y = dst2[i][0][1]
    if x > x_max:
        x_max = x
    if x < x_min:
        x_min = x
    if y > y_max:
        y_max = y
    if y < y_min:
        y_min = y

width = int(x_max - x_min)
height = int(y_max - y_min)

T = np.float32([[1,0, int(abs(x_min))],
                 [0,1, int(abs(y_min))],
                 [0,0,1]])

stitch1 = cv2.warpPerspective(images[0], np.matmul(T,H12), (width, height))
center = cv2.warpAffine(images[1],T[:][:2],(width,height))
mask = np.zeros((512,384),dtype='uint8')
mask = cv2.rectangle(mask,(0,0),(384,512),(255,255,255),3)
mask = cv2.bitwise_not(mask)
alpha = ndimage.distance_transform_edt(mask)
alpha = cv2.resize(alpha,(images[0].shape[1],images[0].shape[0]))
alpha1 = cv2.warpPerspective(alpha, np.matmul(T,H12), (width, height))
alpha2 = cv2.warpAffine(alpha,T[:][:2],(width,height))

a_ = [alpha1,alpha2]
trans_img = [stitch1,center]

result1 = 0
result2 = 0
result3 = 0

np.seterr(invalid='ignore')
for i in range(len(a_)):
    a_sum = sum(a_)
    result1 += ((trans_img[i][:,:,0]*a_[i])/a_sum)
for i in range(len(a_)):
    a_sum = sum(a_)
    result2 += ((trans_img[i][:,:,1]*a_[i])/a_sum)
for i in range(len(a_)):
    a_sum = sum(a_)
    result3 += ((trans_img[i][:,:,2]*a_[i])/a_sum)

result = cv2.merge((result1,result2,result3)).astype('uint8')
result = cv2.cvtColor(result,cv2.COLOR_RGB2BGR)
cv2.imwrite('Stitched Image.jpg',result)
