import os
from os.path import exists
run_string ='python main.py \Images '

os.system('python main.py \Images 12 68')

for minRad in range(30):
    for maxRad in range(20):
        added_string = ''
        added_string += str(minRad)
        added_string += ' '
        added_string += str(maxRad)
        os.system(run_string + added_string)
        old_path = r"output\medium.jpg"
        new_path = r"output\\" + str(minRad) + str(maxRad) + ".png"
        #new_path += str(minRad) + str(maxRad) + ".png"
        print(new_path)
        print(exists(old_path))
        os.rename(old_path, new_path)
    
               
