import numpy as np
'''
@default_height: camera distance from coupon, make sure to set it in image_processor.py if CRTouch not functional
@gantry_width: 210... probably not needed
@y_x: For each change in height, x changes this amount 
@y_z: For each change in height, y changes this amount 
@cam_y: camera y distance 
@cam_x: camera x distance 
'''
class Mover:
    def __init__(self, height = 44.94):
        self.default_height = height
        self.gantry_width = 210
        self.z_x = 1.28 
        self.z_y = 0.685
        self.x_y = 0.533

        self.y_x = 1.28 
        self.y_z = 0.685 

        self.cam_y = self.default_height * self.y_z
        self.cam_x = self.default_height * self.y_x

        self.resol_x =  10
        self.resol_z = 10

        self.sections = self.gantry_width / self.cam_y
        self.cam_width = height * self.z_y 
        self.sections = self.gantry_width / self.cam_width
        
        self.frame_width = self.gantry_width / self.sections

        self.steps_per_section = (self.gantry_width) / self.cam_width
        self.current_frame = 1
        self.resolution_x = 1280 
        self.resolution_y = 720

        #OFFSETS 
        self.x_offset = 145 
        self.z_offset = 50 
        self.tdrx_offset = 23 
        self.tdrz_offset = 26 

        self.local_frame = np.array([[-1000,-1000]])

        
    def add_point(self,point):
        #Frame moved if accepted point is negative 
        if(point == -1):
            self.current_frame += 1

        #Frame virtual position dependent on what frame we are on 
        point[0] = point[0] + (1280 * (self.current_frame - 1))
        point[1] = point[1] + (720 * (self.current_frame - 1))
        
        #Filter out points that are essentially the same 
        match = False
        for comp_point in self.local_frame:
            if(abs(comp_point[1] - point[1]) > 1): #abs(comp_point[0] - point[0]) > 1 and
                continue 
            else:
                match = True
                print("point not accepted: " + str(point))
        if(not match):
            print("Point Added: " + str(point))
            self.local_frame = np.append(self.local_frame,[point], axis=0) 
    
    #Convert points from virtual px to physical to steps
    #May be incorrect since steps 
    def convert_point(self, point):
        cam_width_ratio = self.cam_width/(self.resolution_x * self.current_frame)
        gantry_width_ratio = self.frame_width/(self.resolution_y * self.current_frame)
        print(gantry_width_ratio)
        print(cam_width_ratio)
        converted_point = [point[0] * cam_width_ratio, point[1] * gantry_width_ratio]
        point_x = (converted_point[0]) + self.x_offset - self.tdrx_offset 
        point_z = (converted_point[1]) + self.z_offset - self.tdrz_offset
        converted_point = [point_x, point_z]
        return converted_point

    #Save file as a csv
    def save_file(self):
        self.sort_points()
        print()
        #self.local_frame = np.delete(self.local_frame[0], 1)
        #print(self.local_frame)
        csv_file = open("points.csv","w")
        for point in self.local_frame:
            new_point = self.convert_point(point)
            point_written = str(new_point[0]) + ',' + str(new_point[1]) + '\n'
            csv_file.write(point_written)
        csv_file.close()

        print(self.default_height)
        print(self.cam_x)
        print(self.cam_y)
        return 0 
    
    def sort_points(self):
        #print(self.local_frame)
        #self.local_frame = np.sort(self.local_frame, 1, kind = None, order = None)
        #self.local_frame[self.local_frame[:,1].argsort()]
        #print(self.local_frame)
        return 
        

'''
move = Mover(10) 
move.add_point([1,0])
move.add_point([10,20])
move.add_point([20,30])
move.save_file()
'''