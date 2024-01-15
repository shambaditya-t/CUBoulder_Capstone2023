import os 

class File_Reader:
    def __init__(self):
        self.path = os.getcwd()

    def get_images(self, directory):
        self.path += directory
        return os.listdir(self.path)