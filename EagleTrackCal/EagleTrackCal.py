import libjevois as jevois
import cv2
import numpy as np


upperHue = 100
lowerHue = 0
upperSat = 250
lowerSat = 60
upperVal = 255
lowerVal = 10
errode = 0
dilate = 1
approx = 6
area = 500
solidity = .2



class EagleTrackCal:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("Catbox", 100, jevois.LOG_INFO)
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR by default. If
        # you need a grayscale image instead, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB()
        # and getCvRGBA():
        inimg = inframe.getCvBGR()
        
        # Start measuring image processing time (NOTE: does not account for input conversion time): 
        #Truely useless and can be removed
        self.timer.start()
        #Convert the image from BGR(RGB) to HSV
        hsvImage = cv2.cvtColor( inimg, cv2.COLOR_BGR2HSV)
        
        ## Threshold HSV Image to find specific color
        binImage = cv2.inRange(hsvImage, (lowerHue, lowerSat, lowerVal), (upperHue, upperSat, upperVal))
        
        # Erode image to remove noise if necessary.
        binImage = cv2.erode(binImage, None, iterations = errode)
        #Dilate image to fill in gaps
        binImage = cv2.dilate(binImage, None, iterations = dilate)
        
        #This image is used to display the thresholded image. Bounding Rectangle is added below.
        #Use this image to tune your targeting parameters.
        binOut = cv2.cvtColor(binImage, cv2.COLOR_GRAY2BGR)
        
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
                p = cv2.approxPolyDP(hull, approx, 1)
                if (cv2.isContourConvex(p) != False) and (len(p) == 4) and (cv2.contourArea(p) >= area): #p=3 triangle,4 rect,>=5 circle
                    filled = cnt_area/hull_area
                    if filled <= solidity: #Used to determine if target is hollow or not
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

                cv2.rectangle(binOut, (br[0],br[1]),((br[0]+br[2]),(br[1]+br[3])),(0,0,255), 2,cv2.LINE_AA)




        # Convert our BGR output image to video output format and send to host over USB. If your output image is not
        # BGR, you can use sendCvGRAY(), sendCvRGB(), or sendCvRGBA() as appropriate:
        outframe.sendCvBGR(binOut)
        
        #Write calibration values to a text file named "Calibration" 
        CalFile = open('Calibration', 'w')
        CalFile.truncate()#Clear out old calibraton values
        CalFile.write(str(upperHue))
        CalFile.write(",")
        CalFile.write(str(lowerHue))
        CalFile.write(",")
        CalFile.write(str(upperSat))
        CalFile.write(",")
        CalFile.write(str(lowerSat))
        CalFile.write(",")
        CalFile.write(str(upperVal))
        CalFile.write(",")
        CalFile.write(str(lowerVal))
        CalFile.write(",")
        CalFile.write(str(errode))
        CalFile.write(",")
        CalFile.write(str(dilate))
        CalFile.write(",")
        CalFile.write(str(approx))
        CalFile.write(",")
        CalFile.write(str(area))
        CalFile.write(",")
        CalFile.write(str(solidity))
        
        CalFile.close()#Close calibration file
        
    # ###################################################################################################
    ## Parse a serial command forwarded to us by the JeVois Engine, return a string
    def parseSerial(self, str):
        global upperHue
        global lowerHue
        global upperSat
        global lowerSat
        global upperVal
        global lowerVal
        global errode
        global dilate
        global approx
        global area
        global solidity
        
        jevois.LINFO("parseserial received command [{}]".format(str))
        
        if str == "hello":
            return self.hello()
        
        cal = str.split("=")
        
        if cal[0] == "lowerHue":
            lowerHue = int(cal[1])
            return cal[1]
        
        if cal[0] == "upperHue":
            upperHue = int(cal[1])
            return cal[1]
            
        if cal[0] == "upperSat":
            upperSat = int(cal[1])
            return cal[1]
            
        if cal[0] == "lowerSat":
            lowerSat = int(cal[1])
            return cal[1]
            
        if cal[0] == "upperVal":
            upperVal = int(cal[1])
            return cal[1]
            
        if cal[0] == "lowerVal":
            lowerVal = int(cal[1])
            return cal[1]
            
        if cal[0] == "errode":
            errode = int(cal[1])
            return cal[1]
            
        if cal[0] == "dilate":
            dilate = int(cal[1])
            return cal[1]
            
        if cal[0] == "approx":
            approx = int(cal[1])
            return cal[1]
            
        if cal[0] == "area":
            area = int(cal[1])
            return cal[1]
            
        if cal[0] == "solidity":
            solidity = int(cal[1])/100
            return cal[1]
            
        return "ERR: Fat Fingered that command"
        
            
            
    # ###################################################################################################
    ## Return a string that describes the custom commands we support, for the JeVois help message
    def supportedCommands(self):
        # use \n seperator if your module supports several commands
        return "Use the EagleTuner.py script on a RPi, PC, etc. to send Serial commands to tune the vision tracking."

    # ###################################################################################################
    ## Internal method that gets invoked as a custom command
    def hello(self):
        return "Merry Christmas from EagleForce!"
        


