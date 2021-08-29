import cv2
import numpy as np

class ColourDetector():

    def __init__(self):
        super(ColourDetector, self).__init__()
        self.upperHSV = np.array([0,0,0], np.uint8)
        self.lowerHSV = np.array([0,0,0], np.uint8)

        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        if not(self.cam.isOpened()):
            print("Could not open camera")

        self.filterSetting = 0
        self.displaySetting = 0
        self.trackingSetting = False

    def getProcessedFrame(self):
           
            ret, frame = self.cam.read() # Read the camera frame
            ##Return the raw frame
            if self.displaySetting == 0:
                return None, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            ##Return HSV Frame
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert to HSV

            if self.displaySetting == 1:
                return None, hsvFrame

            ##If image filtering is selected use Gaussian Blurring on HSV Image
            if self.filterSetting == 1 or self.filterSetting == 2:
                filteredhsvFrame = cv2.GaussianBlur(hsvFrame,(5,5),0)
            else:
                filteredhsvFrame = hsvFrame

            ##Return Mask
            mask = cv2.inRange(filteredhsvFrame, self.lowerHSV, self.upperHSV) # Create mask given threshold values

            if self.displaySetting == 2:
                return None, mask

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            ##Set return image
            if self.displaySetting == 3:
                retImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            elif self.displaySetting == 4:
                retImage = hsvFrame
            else:        
                retImage = mask

            
            #If tracking is enabled then find the largest contour and colour it red
            if self.trackingSetting == True:
                largestValues = np.array([-1,-1,-1,-1])
                largestArea = -1
                for c in contours:
                    
                    x,y,w,h = cv2.boundingRect(c)
                    #Check the area of the rectangle
                    area = w*h
                    if area > largestArea:
                        largestArea = area
                        largestValues[:] = ([x,y,w,h])

                    if(self.filterSetting == 2):
                        if not(w < 10 or h < 10):
                            cv2.rectangle(retImage, (x,y), (x+w, y+h), (0,255,0), 2)
                    else:
                        cv2.rectangle(retImage, (x,y), (x+w, y+h), (0,255,0), 2)
                
                if largestArea > -1:
                     cv2.rectangle(retImage, (largestValues[0],largestValues[1]), (largestValues[0]+largestValues[2], largestValues[1]+largestValues[3]), (255,0,0), 2)
            
            else:

                for c in contours:
                 x,y,w,h = cv2.boundingRect(c)
                 if(self.filterSetting == 2):
                    if not(w < 5 or h < 5):
                        cv2.rectangle(retImage, (x,y), (x+w, y+h), (0,255,0), 2)
                 else:
                    cv2.rectangle(retImage, (x,y), (x+w, y+h), (0,255,0), 2)
                
            ##Return image
            if self.trackingSetting == True:
                return largestValues, retImage
            elif self.trackingSetting == False:
                return None, retImage

    def setUpperHSV(self, valArray):
        self.upperHSV = valArray

    def setLowerHSV(self, valArray):
        self.lowerHSV = valArray

    def setDisplaySetting(self, val):
        self.displaySetting = val

    def setFilterSetting(self,val):
        self.filterSetting = val

    def setTrackingSetting(self, val):
        self.trackingSetting = val



