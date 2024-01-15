from PIL import Image 

def merge_images(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)
    result = Image.new("RGB", (result_width, result_height))
    result.paste(im=image1, box=(0,0))
    result.paste(im=image2, box=(width1, 0))
    return result 

merged = merge_images('Stitching/WIN_20230126_11_34_42_Pro.jpg','Stitching/WIN_20230126_11_34_43_Pro.jpg')
merged.save("Result.jpg")