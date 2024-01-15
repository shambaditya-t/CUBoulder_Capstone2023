from PIL import Image, ImageOps
import pytesseract

img = Image.open('viasmalltest.jpg').convert('RGB')

r, g, b = img.split()

img = Image.merge('RGB', (
    r,
    g.point(lambda i: i * 3),  # brighten green channel
    b,
))

img = ImageOps.autocontrast(ImageOps.invert(ImageOps.grayscale(img)), 5)

img.save('vias_processed.png')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print(pytesseract.image_to_string(Image.open("vias_processed.png")))
print(pytesseract.image_to_data(Image.open("vias_processed.png")))
