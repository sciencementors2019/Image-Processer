#Import PIL (pip install pillow) an image manipulation library

from PIL import Image
import glob

#getting list of bmp images
imgs = glob.glob("ImageProcesser\*.bmp")
fils = []
pixelVals = []

#Opening a sample image
for img in imgs:
    fils.append(Image.open(img, 'r'))

#Getting the pixel values
for img in fils:
    pixelVals.append(list(img.getdata()))

#Writing new file
out = open("out.json",'w')
out.write("{\n")
for i in range(len(pixelVals)):
    out.write("\t\"img"+i.__str__()+"\":")
    out.write("\"")
    out.write(pixelVals[i].__str__())
    if pixelVals[len(pixelVals)-1]!=pixelVals[i]:
        out.write("\",\n")
    else:
        out.write("\"")
out.write("\n}")