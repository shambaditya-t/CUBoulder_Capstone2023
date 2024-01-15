import sys
import file_reader as read
import image_process as process
import pytesseract;

def main():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    directory = 0
    try:
        directory = str(sys.argv[1])
        
    except:
        directory = "\Images"
        print("No Directory Provided")
    
    images = read.image_list(directory)

    print(type(int(sys.argv[2])))
    process.run(images,directory,int(sys.argv[2]),int(sys.argv[3]))


if __name__ == "__main__":
    main()
