import libjevois as jevois
import cv2
import numpy as np
import json

#Holders for target data
pixels = [(0,0), (0,0), (0,0), (0,0)]


# Values to use in target distance calculation
Ta = 12 #Actual target width in inches
Fd = 65.0  #Camera View in degrees. JeVois = 65.0, Lifecam HD-300 = 68.5, Cinema = 73.5

##Threshold values for Trackbars, These are pulled from the CalFile
CalFile = open ('Calibration').read().split(",")
uh = int(CalFile[0])
lh = int(CalFile[1])
us = int(CalFile[2])
ls = int(CalFile[3])
uv = int(CalFile[4])
lv = int(CalFile[5])
er = int(CalFile[6])
dl = int(CalFile[7])
ap = int(CalFile[8])
ar = int(CalFile[9])
sl = float(CalFile[10])

#CalFile.close()#Close calibration file

class EagleTrkNoStream:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("Catbox", 100, jevois.LOG_INFO)
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR by default. If
        # you need a grayscale image instead, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB()
        # and getCvRGBA():
        inimg = inframe.getCvBGR()
        
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        #self.timer.start()
        #Convert the image from BGR(RGB) to HSV
        hsvImage = cv2.cvtColor( inimg, cv2.COLOR_BGR2HSV)
        
        ## Threshold HSV Image to find specific color
        binImage = cv2.inRange(hsvImage, (lh, ls, lv), (uh, us, uv))
        
        # Erode image to remove noise if necessary.
        binImage = cv2.erode(binImage, None, iterations = er)
        #Dilate image to fill in gaps
        binImage = cv2.dilate(binImage, None, iterations = dl)
        
                
        ##Finds contours (like finding edges/sides), 'contours' is what we are after
        im2, contours, hierarchy = cv2.findContours(binImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        
        ##arrays to will hold the good/bad polygons
        squares = []
        badPolys = []
        
        ## Parse through contours to find targets
        for c in contours:
            if (contours != None) and (len(contours) > 0):
                cnt_area = cv2.contourArea(c)
                hull = cv2.convexHull(c , 1)
                hull_area = cv2.contourArea(hull)  #Used in Solidity calculation
                p = cv2.approxPolyDP(hull, ap, 1)
                if (cv2.isContourConvex(p) != False) and (len(p) == 4) and (cv2.contourArea(p) >= ar):
                    filled = cnt_area/hull_area
                    if filled <= sl:
                        squares.append(p)
                else:
                    badPolys.append(p)
        
        ##BoundingRectangles are just CvRectangles, so they store data as (x, y, width, height)
        ##Calculate and draw the center of the target based on the BoundingRect
        for s in squares:        
            br = cv2.boundingRect(s)
            #Target "x" and "y" center 
            x = br[0] + (br[2]/2)
            y = br[1] + (br[3]/2)

            
        for s in squares:
            if len(squares) > 0:
                #Build "pixels" array to contain info desired to be sent to RoboRio
                pixels = {"Trk" : 1, "XCntr" : x, "YCntr" : y}
                json_pixels = json.dumps(pixels)

                
        if not squares:
            pixels = {"Trk" : 0, "XCntr" : 0, "YCntr" : 0}
            json_pixels = json.dumps(pixels)
            
        jevois.sendSerial(json_pixels)
        
