from imagePInternals import *

#Initializes the image processer to process 'HoloSquare2.bmp' and 
image = imageProcesser('HoloSquare2.bmp')

#Prints detail of the image
image.detail()
#Shows the image with cv2.imshow()
image.show()

#Returns the serialized image
image.serialize()