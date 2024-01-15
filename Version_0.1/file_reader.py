'''
File Reader
'''
import os


def image_list(directory):
    path = os.getcwd()
    path += directory
    images = os.listdir(path)
    return images

