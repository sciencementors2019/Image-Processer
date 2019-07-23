from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import math
import glob
import pickle

class dataBundle:
    def __init__(self):
        self.images = []
    
    def addImage(self, image):
        self.images.append(image)

    def serialize(self):
        pickle.dump(self, open("bundle.p", "wb"))
        return pickle.dumps(self)

    def deserialize(self):
        return pickle.load(open('bundle.p', 'rb'))

    def getData(self):
        return self.images


class imageProcesser:
    def __init__(self, filename):
        self.filename=filename
        self.img=cv2.imread(self.filename)
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.thresh = cv2.threshold(self.gray,127,255,1)[1]
        self.contours,h = cv2.findContours(self.thresh,1,2)
    #warning you are now entering a bruh moment zone
    def serialize(self):
        pickle.dump(self, open("out.p", "wb"))
        return pickle.dumps(self)
    #warning you are now exiting a bruh moment zone
    def readPickle(self):
        return pickle.load(open('out.p', 'rb'))

    def show(self):
        cv2.imshow('img',self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detail(self):
        #Prints the results to screen
        for cnt in self.contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            #approx is used for specific functions, cnt is used for the drawing.
            print(len(approx))
            
            self.getCorners(approx)
            self.getOrientation(cnt)
            if len(self.getEdgeLengths(approx)) < 9:
                print(self.getEdgeLengths(approx))
                
            if len(self.DistanceFromCentre(approx)) < 9:
                
                print(self.DistanceFromCentre(approx))
            else:
                print(self.DistanceFromCentre(approx))
            cv2.drawContours(self.img,[cnt],0,(1,1,1),-1)

    #Both Functions get the relative angle, both work to varying levels of success
    def getAngleDP(self, p1, p2):
        len1 = math.sqrt(p1[0]**2 + p1[1]**2)
        len2 = math.sqrt(p1[0]**2 + p1[1]**2)
    #Dot product is the point between the two contours being compared
        dot = p1[0] * p2[0] + p1[1] + p2[1]

        angle = dot / (len1 * len2)

        return math.acos(angle) * 180 / math.pi

    def getAngleAtan(self, p1, p2):
        #atan2 gets the angle of the contour, but is extremely relative to the orientation of the object
        angle = math.atan2((p1[1] - p2[1]) , (p1[0] - p2[1])) * 180 / math.pi
        return angle
        
    #Gets the angles in the shape, isn't working too well right now.
    def sumOfAngles(self, contours):

        conRect = []
        for i in range(len(contours)):
            conBB = cv2.minAreaRect(contours[i])
            
            conRect.append(conBB[0])
        AngleSet = []
        for i in range(len(conRect)):
            if i+1 >= len(conRect):
                Length1 = conRect[i-len(conRect)]
                Length2 = conRect[i]
            else:
                Length1 = conRect[i-1]
                Length2 = conRect[i+1]

            Angle = self.getAngleDP(Length1, Length2)
            AngleSet.append(Angle)

        return AngleSet
    #Gets the overall rotation of the shape, spanning from -180 to 180
    def getOrientation(self, contour):

        rect = cv2.minAreaRect(contour)
        print(rect[2])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        height_px_1 = box[0][1] - box[3][1]
        height_px_2 = box[1][1] - box[2][1]
        

        if height_px_1 < height_px_2:
            close_height_px = height_px_2
            far_height_px = height_px_1
        else:
            close_height_px = height_px_1
            far_height_px = height_px_2

        return rect[2]
        
    #Marks the vertices of the shape, can be used to get the number of them as well
    def getCorners(self, contours):
        corners = 0
        for i in range(len(contours)):
            rect = cv2.minAreaRect(contours[i])
            center = rect[0]
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(self.img,[box],0,(255,0,0),2)
            corners += 1
            
        return corners
    #Gets the centre of an entire object based on contour        
    def getCentre(self, contour):
        M = cv2.moments(contour)    
        
        cX = int(M["m10"] / M["m00"]) #TODO: Can get a zero division error  make try and catch
        cY = int(M["m01"] / M["m00"])
        return cX, cY
        
    #Gets the distance of each corner(I think) to the centre of the shape
    def DistanceFromCentre(self, contours):
        conRect = []
        try:
            centrePoint = self.getCentre(contours)
        except:
            centrePoint = [0,0]
        for i in range(len(contours)):
            conBB = cv2.minAreaRect(contours[i])
            
            conRect.append(conBB[0])
        disFromCentre = []
        for i in range(len(conRect)):
            Corner = conRect[i-1]

            Hypot = np.sqrt((Corner[0] - centrePoint[0])**2 + (Corner[1] - centrePoint[1])**2)
            disFromCentre.append(Hypot)
            
        return disFromCentre
    #Gets the length of each edge and compiles them into a list
    def getEdgeLengths(self, contours):
        conRect = []
        for i in range(len(contours)):
            conBB = cv2.minAreaRect(contours[i])
            
            conRect.append(conBB[0])
        conLength = []
        for i in range(len(conRect)):
            Length1 = conRect[i-1]
            Length2= conRect[i]


            Hypot = np.sqrt((Length1[0] - Length2[0])**2 + (Length1[1] - Length2[1])**2)
            conLength.append(Hypot)
            
        return conLength
    #Checks if Edge lengths are equal, doesn't work well with circles
    def ifEdgeLengthsEqual(self, contours):

        Edges = (self.getEdgeLengths(contours))
            
        if len(Edges) == 4:
            if len(np.unique(Edges)) == 2:
                return "Rectangular"
            if len(np.unique(Edges)) == 1:
                return "Square"
            if len(np.unique(Edges)) > 2:
             return "Quadlilateral"
            
        if len(Edges) == 3:
            if len(np.unique(Edges)) == 1:
                return "EquilateralTriangle"
            if len(np.unique(Edges)) == 2:
                return "IsoscelesTriangle"
            if len(np.unique(Edges)) == 3:
                return "Triangle"