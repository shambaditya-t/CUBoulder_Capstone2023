import cv2
import numpy as np
import pytesseract
import shutil
import os
import random
import time
import math
import logging 
import threading
import time 
import gantry_mover
import gantry_mover2
import gantry_mover3
class Executor:
    def __init__(self, cr_data, iteration):

        self.path = os.getcwd()
        self.full_path = ''


        self.vid = cv2.VideoCapture(0)                  #Initializing video capture      
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)    #Setting X max resolution to 1280px
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)    #Setting Z max resolution to 720

        self.par1 = 50                                  #Controls sensitivity of edge, too high wont detect enough
        self.par2 = 70                                  #Sets how many edge points it needs to detect
        self.min_Rad = 0                                #Smallest Size for Circles 
        self.max_Rad = 20                               #Largest Radius for Circles

        self.cr_data = cr_data                          #BL_Touch Data
        self.iteration = iteration                      #Which stage are we in
        self.reg_matrix = np.matrix([[[0,0],[0,0]],[[0,0]],[[0,0]]], dtype = object)    #Matrix to keep track of hough circles

        

        self.mover = gantry_mover.Mover(44.94)          #Old Gantry Mover Code, Defunct 
        self.mover2 = gantry_mover2.Collector(43.99,iteration)    #New Gantry Mover Code 
        self.mover3 = gantry_mover3.Collector(43.99,iteration)
        self.timer_val = False
    
    def counter_thread(self, none):
        time.sleep(10)
        self.timer_val = True
        return True
    def test_thread(self, none):
        #self.reg_matrix
        print(self.reg_matrix)
        print("Hello?")
        '''
        while self.par1 > 50:
            time.sleep(1)
            self.par1 -= 1
            print("PAR2: " + str(self.par1))
        '''
        '''
        while self.min_Rad > 0:
            time.sleep(1)
            self.min_Rad -= 1
            print("MIN RAD: " + str(self.min_Rad))
        
        '''

        '''
        self.min_Rad = 8 
        
        while self.max_Rad < 40:
            time.sleep(1)
            self.max_Rad += 1
            print("MAX RAD: " + str(self.max_Rad))
        '''
        
    
    def apply_gray(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def apply_Gaussian(self,image):
        new_image = cv2.GaussianBlur(image, (5,5), 0)
        return new_image
    
    def apply_canny(self,image):
        canny_image = cv2.Canny(image=image, threshold1=100, threshold2=200)
        return canny_image

    def create_csv(self, array):
        return 0
    def apply_via_detection(self, image):
        circ_array = np.array([0,0], dtype = object)
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1.5,20,param1=self.par1,
                               param2=self.par2,minRadius=self.min_Rad,maxRadius=self.max_Rad)
        
        try:
            circles = np.uint16(np.around(circles))
            
            for i in circles[0,:]:
                #cv2.circle(image,center_coordinates,radius,color,thickness)
                circle = [i[0],i[1]]
                circ_array = np.append(circ_array, circle)

                #self.mover.add_point(circle)
                #self.mover2.add_point(circle[0],circle[1])
                self.mover3.add_point(circle[0],circle[1])
                #print([i[0],i[1]])
                cv2.circle(image,(i[0],i[1]),i[2],(0,0,255),10)
                cv2.circle(image,(i[0],i[1]),2,(0,255,0),10)
            #print(circ_array)
            new_shape = len(circ_array)/2
            new_shape = math.floor(new_shape)
            circ_array = np.reshape(circ_array,[new_shape,2])
            np.savetxt("test.csv"[:-4] + ".csv", circ_array, delimiter=',')
            return image
        except Exception as e:
            #print(e)
            #print("Error: No Via Holes Detected")
            return image

    def run_process(self,image):
        image = self.apply_gray(image)
        image = self.apply_via_detection(image)
        return image

    def run(self, image_list, directory):
        thread_runner = threading.Thread(target=self.test_thread, args=(1,))
        thread_runner.start()

        timer = threading.Thread(target=self.counter_thread, args=(1,))
        timer.start()
        self.full_path = self.path + directory 
        while(True):
            ret, frame = self.vid.read()
            edit_frame = self.run_process(frame)
            cv2.imshow('frame', edit_frame)
        
            if ((cv2.waitKey(1) & 0xFF == ord('q')) or self.timer_val):
                #self.mover2.save_points()
                self.mover3.run_collector()
                
                break
               
            if cv2.waitKey(1):
                self.mover2.save_points
        self.vid.release()
        cv2.destroyAllWindows() 


        


        