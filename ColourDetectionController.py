from ServoController import ServoController
from ColourDetectionModel import ColourDetector
from ColourDetectionView import DetectionView
import threading
import time

class DetectorController(threading.Thread):

    def __init__(self, colourDetector, view, servoController, group=None, target=None, name='DetectControllerThread', 
                args=(), kwargs=None, verbose=None):

        super(DetectorController, self).__init__()
        self.target = target
        self.name = name
        self.cd = colourDetector
        self.view = view
        self.running = False #Flag to control thread operation 
        self.servoController = servoController

    def run(self):
        self.running = True
        while True:
            result, frame = self.cd.getProcessedFrame(None)
            self.view.addFrame(frame)
            #Check if the HSV Values have changed
            if self.view.hsvChanged() == True:
                newHSV = self.view.getHSVValues()
                self.cd.setUpperHSV(newHSV[0:3])
                self.cd.setLowerHSV(newHSV[3:6])
            #Check if the display settings have changed
            if self.view.dsChanged() == True:
                newSetting = self.view.getDisplaySetting()
                self.cd.setDisplaySetting(newSetting)

            #Check if the filter settings have changed
            if self.view.fsChanged() == True:
                newSetting = self.view.getFilterSetting()
                self.cd.setFilterSetting(newSetting)

            ##Check if the tracking settings have changed
            if self.view.trChanged() == True:
                newSetting = self.view.getTrackingSetting()
                self.cd.setTrackingSetting(newSetting)

            ##Check if the gui window has closed
            if self.view.running is False:
                break

            ##Move servo values based on the position of the center of the largest contour
            if result is not None:
                if result[0] is not -1:
                    self.trackLargestContour(result, 0.01)

            time.sleep(0.001)


    def trackLargestContour(self, result, speedValue):

        #Calculate centre point of rectangle
        recCentreX = result[0] + round(result[2]/2)
        recCentreY = result[1] + round(result[3]/2)
        
        #Calculate centre point position relative to the centre of the camera frame
        frameCentreX = 320
        frameCentreY = 240
        
        #Move left or right
        if recCentreX > (frameCentreX + 20):
            self.servoController.moveAlongX(speedValue)
        elif recCentreX < (frameCentreX - 20):
            self.servoController.moveAlongX(-speedValue)
        
        #Move up or down 
        if recCentreY > (frameCentreY + 20):
            self.servoController.moveAlongY(speedValue)
        elif recCentreY < (frameCentreY - 20):
            self.servoController.moveAlongY(-speedValue)
