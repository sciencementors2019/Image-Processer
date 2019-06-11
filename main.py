#Import PIL (pip install pillow) an image manipulation library

from PIL import Image
import glob

#getting list of bmp images
imgs = glob.glob("./*.bmp")
fils = []
pixelVals = []

#Opening images
for img in imgs:
    pixelVals.append([])
    fils.append(Image.open(img, 'r'))

#Getting the pixel values and appending them to pixelvals list
for img in fils:
    img.convert('RGB')
    width, height = img.size
    for i in range(0,width):
        for j in range(0,height):
            r = img.getpixel((i,j))
            for i in range(len(fils)):
                if img == fils[i]:
                    pixelVals[i].append(r)
            
print(pixelVals) #for debugging
#Opening out.json
out = open("out.json",'w')
out.write("{\n") #writing the first {
for i in range(len(pixelVals)):
    out.write("\t\"img"+i.__str__()+"\":") #Write the image index e.g. "img0"
    out.write(pixelVals[i].__str__())
    if pixelVals[len(pixelVals)-1]!=pixelVals[i]:
        out.write(",\n") #just do a comma and then a new line
    else:
        out.write("") #TODO: replace out.write("") with pass
out.write("\n}") #writing the ending }