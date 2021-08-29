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


    def getProcessedFrame(self):
            print(self.upperHSV)
            print(self.lowerHSV)
            ret, frame = self.cam.read() # Read the camera frame
            ##Return the raw frame
            if self.displaySetting == 0:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            ##Return HSV Frame
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert to HSV

            if self.displaySetting == 1:
                return hsvFrame

            ##If image filtering is selected use Gaussian Blurring on HSV Image
            if self.filterSetting == 1 or self.filterSetting == 2:
                filteredhsvFrame = cv2.GaussianBlur(hsvFrame,(5,5),0)
            else:
                filteredhsvFrame = hsvFrame

            ##Return Mask
            mask = cv2.inRange(filteredhsvFrame, self.lowerHSV, self.upperHSV) # Create mask given threshold values

            if self.displaySetting == 2:
                return mask

            contours, heirachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            ##Set return image
            if self.displaySetting == 3:
                retImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            elif self.displaySetting == 4:
                retImage = hsvFrame
            else:        
                retImage = mask
            for c in contours:
                 x,y,w,h = cv2.boundingRect(c)
                 if(self.filterSetting == 2):
                    if not(w < 5 or h < 5):
                        cv2.rectangle(retImage, (x,y), (x+w, y+h), (0,255,0), 2)
                 else:
                    cv2.rectangle(retImage, (x,y), (x+w, y+h), (0,255,0), 2)
                

            ##Return image
            return retImage

    def filterBinaryMask(mask):
        mask

        return

    def setUpperHSV(self, valArray):
        self.upperHSV = valArray

    def setLowerHSV(self, valArray):
        self.lowerHSV = valArray

    def setDisplaySetting(self, val):
        self.displaySetting = val

    def setFilterSetting(self,val):
        self.filterSetting = val

    