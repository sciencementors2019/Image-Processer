#Import PIL (pip install pillow) an image manipulation library

from PIL import Image

#Opening a sample image
img = Image.open('D:/Science Mentors 2019/ImageProcesser/pointillist.bmp', 'r')

#Getting the pixel values
pixelVals = list(img.getdata())

#Writing new file
out = open("out.txt",'w')
out.write(pixelVals.__str__())