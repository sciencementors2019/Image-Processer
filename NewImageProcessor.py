from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import math

#Initialises Image settings
img = cv2.imread('HoloSquare2.bmp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,127,255,1)

contours,h = cv2.findContours(thresh,1,2)

#Both Functions get the relative angle, both work to varying levels of success
def getAngleDP(p1, p2):
    len1 = math.sqrt(p1[0]**2 + p1[1]**2)
    len2 = math.sqrt(p1[0]**2 + p1[1]**2)
#Dot product is the point between the two contours being compared
    dot = p1[0] * p2[0] + p1[1] + p2[1]

    angle = dot / (len1 * len2)

    return math.acos(angle) * 180 / math.pi

def getAngleAtan(p1, p2):
#atan2 gets the angle of the contour, but is extremely relative to the orientation of the object
   angle = math.atan2((p1[1] - p2[1]) , (p1[0] - p2[1])) * 180 / math.pi
   return angle
    
#Gets the angles in the shape, isn't working too well right now.
def sumOfAngles(contours):

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

        Angle = getAngleDP(Length1, Length2)
        AngleSet.append(Angle)

    return AngleSet
#Gets the overall rotation of the shape, spanning from -180 to 180
def getOrientation(contour):

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
def getCorners(contours):
    corners = 0
    for i in range(len(contours)):
        rect = cv2.minAreaRect(contours[i])
        center = rect[0]
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img,[box],0,(255,0,0),2)
        corners += 1
        
    return corners
#Gets the centre of an entire object based on contour        
def getCentre(contour):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return cX, cY
    
#Gets the distance of each corner(I think) to the centre of the shape
def DistanceFromCentre(contours):
    conRect = []
    centrePoint = getCentre(contours)
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
def getEdgeLengths(contours):
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
def ifEdgeLengthsEqual(contours):

    Edges = (getEdgeLengths(contours))
        
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
#Prints the results to screen
for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    #approx is used for specific functions, cnt is used for the drawing.
    print(len(approx))
    
    getCorners(approx)
    getOrientation(cnt)
    if len(getEdgeLengths(approx)) < 9:
        print(getEdgeLengths(approx))
        
    if len(DistanceFromCentre(approx)) < 9:
        
        print(DistanceFromCentre(approx))
    else:
        print(DistanceFromCentre(approx)[0])
    cv2.drawContours(img,[cnt],0,(1,1,1),-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

