import os

from PIL import Image

imagepath = os.path.realpath("images")
image_list = os.listdir(imagepath)
destination_path = "./opt/icons"
for image in image_list:
    open_image = Image.open(image)
    transposed = open_image.transpose(open_image.ROTATE_90)
    resized_image = transposed.resize(128, 128)
    resize_image.save(str(destination_path + image))
