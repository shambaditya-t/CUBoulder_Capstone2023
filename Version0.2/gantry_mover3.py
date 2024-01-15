from point import Point
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

class THRESH(Enum):
    XTHRESH = 1
    YTHRESH = 2

class CONSTRAINT(Enum):
    XMAX = 160
    XMIN = 150 
    YMAX = 0
    YMIN = 0


class Collector:
    def __init__(self, height, iteration):
        self.height = height                                            #Height of camera from the coupon
        self.camx = height * RATIO.XY.value                             #Camera x distance in real space 
        self.camz = height * RATIO.ZY.value                             #Camera z distancei n real space 

        self.camx_convert = self.camx/RESOLUTION.XRESOL.value           #Conversion from px to mm. Multiply value in px by this to get mm 
        self.camz_convert = self.camz/RESOLUTION.ZRESOL.value     

        self.frame = np.array([[]])                                     #Empty Array to hold all points 
        self.iteration = iteration  

        self.points = []        #Test

        self.set_high = []
        self.set_low = []
        self.avg_high = 0

        self.const_offset = 2.7
        

    def run_collector(self):
        self.convert_all()                              #Convert all received points into physical points
        self.order_points(self.points)                  #Order points from start to end
        self.remove_points()                            #Remove points that are out of bounds or improper
        self.print_points(self.points)                  #Print out all the points in the 
        self.split_set()
        #self.print_points(self.set_low)
        self.clean_points(self.set_high)
        self.clean_points(self.set_low)
        #self.print_points(self.points)
        self.write_points()


    '''
    @add_Point
    @input:
        pointx: The pixel value of the x point 
    '''
    def add_point(self,pointx,pointz):
        input_point = Point(pointx,pointz+ (RESOLUTION.ZRESOL.value * (self.iteration-1)))
        
        if(len(self.points) == 0):
            self.points.append(input_point)
            return 0
        
        for point in self.points:
            if(abs(point.x_val - input_point.x_val) < THRESH.XTHRESH.value):
                if(abs(point.y_val - input_point.y_val) < THRESH.YTHRESH.value):
                    point.confidence += 1
                    return 0
        self.points.append(input_point)

    def remove_points(self):
        valid_points = []
        for point in self.points:
            if(point.confidence > 0):
                if(point.x_val > CONSTRAINT.XMIN.value and point.x_val < CONSTRAINT.XMAX.value):
                    valid_points.append(point)
            
        self.points = valid_points



    def order_points(self, set):
        set.sort(key=lambda x: x.y_val)

    def split_set(self):
        std_calc = self.find_std(self.points)
        #self.print_points(self.points)
        std_x = std_calc[0]
        average_x = std_calc[1]
        print("Standard:" + str(std_x))
        #If the standard deviation is over 0.5, we know that there are most likely two sets 
        if(std_x > 1.5):
            print("ENTERED")
            comparison_low = average_x-std_x
            comparison_high = average_x + std_x
            
            for point in self.points:
                if(abs(comparison_low - point.x_val) < abs(comparison_high - point.x_val)):
                    self.set_low.append(point)
                else:
                    self.set_high.append(point)
        else:
            self.set_high = self.points
            self.set_low = []
            self.clean_high()
            return 0
        self.clean_high()
        self.clean_low()
    
    def find_std(self,set):
        '''
        Calculate Standard Deviation for X and Y values
        '''
        sum_x = 0
        average_x = 0
        std_x = 0

        sum_y = 0
        average_y = 0
        std_y = 0

        num_points = len(set)

        for point in set:
            sum_x += point.x_val
            sum_y += point.y_val
        
        average_x = sum_x/num_points
        average_y = sum_y/num_points

        for point in set:
            std_x += (point.x_val-average_x)**2
            std_y += (point.y_val-average_y)**2

        std_x = (std_x/(num_points - 1))**(1/2)
        std_y = (std_y/(num_points - 1))**(1/2)
        return [std_x,average_x]
    def clean_points(self,set):
        remove_list = []
        for i in range(0,len(set) - 1):
            if(abs(set[i].y_val-set[i+1].y_val) < 2):
                remove_list.append(set[i])
        for point in remove_list:
            set.remove(point)

    def clean_high(self):
        std_calc = self.find_std(self.set_high)
        self.avg_high = std_calc[1]
        for point in self.set_high:
            point.x_val = std_calc[1]  #Set to average

        
            
        
    def clean_low(self): 
        std_calc = self.find_std(self.set_low)
        for point in self.set_low:
            point.x_val = std_calc[1]  #Set to average
            '''
            if(abs(point.x_val-self.avg_high) > 3):
                #self.set_low.remove(point)
                remove_list.append(point)
            '''


    def convert(self,point):
        point.x_val = (-1 * point.x_val * self.camx_convert) + OFFSET.XGENERAL.value + OFFSET.TDRX.value - 5.9
        point.y_val = (point.y_val * self.camz_convert) + OFFSET.ZGENERAL.value + OFFSET.TDRZ.value + OFFSET.UNCERTAIN.value - 1.1
        
        point.x_val = round(point.x_val,2)
        point.y_val = round(point.y_val,2)

    def convert_all(self):
        for point in self.points:
            self.convert(point)
            
    def print_points(self,set):
        i = 0
        for point in set:
            i += 1
            print("Point " +  str(i) + ": (" + str(point.x_val) + "," + str(point.y_val) + "," + str(point.confidence) + ")")
    def write_points(self):
        csv_file = open("points.csv","a")
        first_point = True
        first_point_z = 0
        for point in self.set_high:
            if(first_point):
                first_point = False
                first_point_z = point.y_val
            point_written = str(point.x_val + 0.8) + ',' + str(self.adjust_pt(point,2.7,first_point_z)) + '\n'
            csv_file.write(point_written)
        if(len(self.set_low) != 0):
            csv_file.write("-1,-1\n")
            self.adjust_low_to_high()
            for point in self.set_low:
                point_written = str(point.x_val + 3.35) + ',' + str(self.adjust_pt(point,2.7,self.set_low[0].y_val)) + '\n'
                csv_file.write(point_written)
        
        csv_file.write("-1,-1\n")

        csv_file.close()


    def adjust_pt(self, point, offset, initial_point_val):
        point_x = point.y_val - initial_point_val
        beta = point_x/offset
        beta = round(beta)
        new_x = (beta * offset) + initial_point_val
        return new_x
    
    def adjust_low_to_high(self):
        for i in range(0,len(self.set_low)):
            for j in range(0,len(self.set_high)):
                if(abs(self.set_high[j].y_val - self.set_low[i].y_val) < 0.5):
                    print("Changed")
                    self.set_low[i].y_val = self.set_high[j].y_val
                    print(str(self.set_low[i].y_val) + ":" + str(self.set_high[j].y_val))
'''
test = Collector(10,10)
test.add_point(190,460)
test.add_point(308,398)
test.add_point(244,161)
test.add_point(305,223)
test.add_point(310,577)
test.add_point(308,461)
test.add_point(196,692)
test.add_point(311,692)
test.add_point(310,520)
test.add_point(307,341)
test.add_point(194,692)
test.add_point(311,635)
test.add_point(194,637)
test.add_point(310,692)
test.add_point(310,575)
test.add_point(310,517)
test.add_point(311,637)
test.add_point(187,281)
test.convert_all()
test.split_set()
test.print_points(test.points)
'''