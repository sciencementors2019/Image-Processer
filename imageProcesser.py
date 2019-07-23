from imagePInternals import *

#Initialize the data bundle
bundle = dataBundle()

#Initializes the image processer to process 'HoloSquare2.bmp' and 
holosquare = imageProcesser('HoloSquare2.bmp')

#Initializes the image processer to process 'flow.bmp' and 
flow = imageProcesser('dfg.jpg')

#Adds the processed image data to the bundle
bundle.addImage(holosquare)
bundle.addImage(flow)

#Serializes the bundle
bundle.serialize()

#Prints the unserialized data
bundle.getData()

#Gets the serialized class and deserializes it
newbundle = bundle.deserialize()

#No need to deserialize imageProcesser as it is part of dataBundle object
newbundle.getData()[0].show()
newbundle.getData()[0].detail()
newbundle.getData()[0].show()