import numpy as np 
from enum import Enum

class RATIO(Enum):
    XY = 1.28           #X = 1.28Y
    ZY = 0.685          #Z = 0.685Y
    ZX = 0.533          #Z = 0.533X 

class OFFSET(Enum):
    XGENERAL = 122      #Offset from 0 to reach (0,0) for x
    ZGENERAL = 69       #Offset from 0 to reach (0,0) for z 
    TDRX = 47           #Offset to get TDR probe to (0,0) for x
    TDRZ = -45          #Offset to get TDR probe to (0,0) for x
    UNCERTAIN= 2
    
class RESOLUTION(Enum):
    XRESOL = 1280
    ZRESOL = 720

class Collector:
    '''
    '''
    def __init__(self, height, iteration):
        self.height = height                                            #Height of camera from the coupon
        self.camx = height * RATIO.XY.value                             #Camera x distance in real space 
        self.camz = height * RATIO.ZY.value                             #Camera z distancei n real space 

        self.camx_convert = self.camx/RESOLUTION.XRESOL.value           #Conversion from px to mm. Multiply value in px by this to get mm 
        self.camz_convert = self.camz/RESOLUTION.ZRESOL.value     

        self.frame = np.array([[]])                                     #Empty Array to hold all points 
        self.iteration = iteration                                      #Which iteration are we on 

    def add_point(self,pointx,pointz):
        reject = False                                                  #Boolean to keep track of point rejection
        thresholdX = 1                                                  #Allowable distance between points                             
        thresholdZ = 2
        point = np.array([[pointx,pointz + (RESOLUTION.ZRESOL.value * (self.iteration-1))]])                             #Point Defined as a numpy array
        #print(pointx + (RESOLUTION.XRESOL.value * self.iteration))
        #(RESOLUTION.XRESOL.value * self.iteration)
        if(self.frame.size == 0):
            self.frame = np.concatenate((self.frame,point),axis=1)      #First point is always accepted, so that we can actually make comparisons 
        else:
            '''
            Can't accept every points, filter out based on Z axis value, as they should not be identical
            '''
            for i in range(1,self.frame.size,2):                        
                if(abs(self.frame[0][i] - point[0,1]) > thresholdX):             #Compare absolute difference based on threshold 
                    if(abs(self.frame[0][-1]-point[0,0]) > thresholdZ):
                        continue
                    else:
                        reject = True
                else:
                    reject = True

        if(not reject):         
            self.frame = np.concatenate((self.frame,point),axis=1)              #Add point to the list 
        
    def reshape(self):
        #print(int(np.size(self.frame)/2))
        self.frame = self.frame.reshape(int(np.size(self.frame)/2),2)
       

    def filter(self,m=0.5):
        '''
        FILTER BASED ON SMALL STD OF X 
        '''
        print("Pre Sorted")
        #print(self.frame)
        median = np.median(self.frame,axis=0)                           #Median of points returned as [medianX, medianZ]
        mean = np.mean(self.frame,axis=0)                               #Mean of points returned as [meanX,meanZ] 
        std = np.std(self.frame,axis=0)                                 #Standard Deviation returned as [stdX, stdY]
        deviation = np.abs(self.frame-np.mean(self.frame,axis=0))       #Calculation of how far from the mean each points is 
        allow_deviate = m*std                                           #Number of standard deviations we're allowed to deviate by
        
        self.frame = self.frame[deviation[0:,0] < allow_deviate[0]]     #X axis filtered to a very strict degree (test points shouldn't vary much)
        
        self.frame = self.frame[self.frame[:,1].argsort()]              #Sorting the points based on the Z axis
        print("Sorted")
        #print(self.frame) 
        count = 0      
        for point in self.frame:
            #print(self.frame[count,0])     
            self.frame[count,0] = median[0];   
            count += 1                          

        '''
        FILTER Z VALUES 
        need to document better
        '''      
        thresholdZ = 2 * (RESOLUTION.ZRESOL.value/self.camz)                     #Threshold for allowable difference between Z points, converted from mm to px
        keep = np.array([[]])                                                    #Had issues with array deletions, will have kept positions in here
        for i in range(0,(int(self.frame.size/2))-1):                            #Compare array i with array i+1, if beyond threshold, don't adad
            if(abs(self.frame[i][1] - self.frame[i+1][1]) > thresholdZ):
                keep = np.concatenate((keep,np.array([self.frame[i]])),axis=1)
        #Y = X[X[:, 2].argsort()]
        self.frame = keep.reshape(int(np.size(keep)/2),2)                        #Set frame to the new keep multi-dim array

        

    def convert(self,point):
        x_convert = (-1 * point[0] * self.camx_convert) + OFFSET.XGENERAL.value + OFFSET.TDRX.value - 2.63 - OFFSET.UNCERTAIN.value   #Convert X value to mm, then apply offset translation 
        z_convert = (point[1] * self.camz_convert) + OFFSET.ZGENERAL.value + OFFSET.TDRZ.value + OFFSET.UNCERTAIN.value - 1.4  #Convert Z value to mm, then apply offset translation 

        return [x_convert,z_convert]   
    #Document this better................................
    def save_points(self,round_to=2):
        self.reshape()
        self.filter()
        
        csv_file = open("points.csv","a")
        point_val = -1
        first_point_z = 0
        for point in self.frame:

            if(point_val == -1):                                                         #Added
                first_point_z = self.convert(point)[1]
                
            point_val += 1                                                              #Point val used to multiply by change required
            new_point = self.convert(point)
            new_point[1] = first_point_z + (2.72*point_val)                             #Added
        

            new_point = np.round(new_point,round_to)
            point_written = str(new_point[0]) + ',' + str(new_point[1]) + '\n'
            csv_file.write(point_written)
        csv_file.close()

        

''' 
gan = Collector(10)
gan.add_point(50.4,20)
gan.add_point(50.5,40)
gan.add_point(50,60)
gan.add_point(50.1,20)
gan.add_point(50.6,40)
gan.add_point(50.2,60)
gan.add_point(50.9,20)
gan.add_point(50.1,40)
gan.add_point(50.4,20)
gan.add_point(50.5,40)
gan.add_point(50,60)
gan.add_point(50.1,20)
gan.add_point(50.6,40)
gan.add_point(50.2,60)
gan.add_point(50.9,20)
gan.add_point(50.1,40)
gan.add_point(52,60)
gan.add_point(53,1221)
gan.add_point(54,12312)
gan.save_points(round_to=2)
'''