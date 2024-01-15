import sys 
import file_sys
import image_processor
import io
import serial
from serial.tools import list_ports
import bl_server
import os

def main():
    iteration = 0
    try:
        iteration = int(sys.argv[1])
        print("Iteration: " + str(iteration))
        if(iteration == 1 and os.path.isfile("points.csv")):
            os.remove("points.csv")
    except:
        print("Didn't Receive Proper Argument (Specify Stage Number)")
        return 0
    server = bl_server.BL_Server(8080)              #Defining UDP Server 
    image_reader = file_sys.File_Reader()           #Defunct File Reader Defined (potentially needed for stitching...)
    directory = '\Images'                           
    images = image_reader.get_images(directory)
    #print(images)


    cr_z_data = server.recv_height(False)           #Receive height data from BL_Touch(Condition indicates if UDP Server is should be activated)
    executor = image_processor.Executor(cr_z_data,iteration)  #Start Image Processing

    #Running Program
    executor.run([],'')
    



if __name__ == "__main__":
    print("______________________Starting Computer Vision Software_______________________")
    print("V_3")
    main()
    '''
    selection = input("Please Choose Manual(M) or Automatic Command Mode(A): ")


    
    if(selection == 'M' or selection == 'm' or selection == "Manual" or selection == "manual"):
        print("Entering Manual Command")
        print("Please choose a COM port from the following list (e.g. COM6)")
        sel = input('\n'.join([', '.join([d.name, d.manufacturer or '', d.product or '']) for d in list_ports.comports()]))
    elif(selection == 'Automatic' or selection == 'A' or selection == 'a' or selection == 'automatic'):
        print("Entering Automatic Impedance Mode, starting test")
        main()
   '''