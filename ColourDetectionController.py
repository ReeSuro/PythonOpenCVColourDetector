from ColourDetectionModel import ColourDetector
from ColourDetectionView import DetectionView
import numpy as np
import threading

class DetectorController(threading.Thread):

    def __init__(self, colourDetector, view, group=None, target=None, name='DetectControllerThread', 
                args=(), kwargs=None, verbose=None):

        super(DetectorController, self).__init__()
        self.target = target
        self.name = name
        self.cd = colourDetector
        self.view = view
        self.running = False

    def run(self):
        print("Controller Running")
        self.running = True
        while True:
            print("Calling get frame")
            frame = self.cd.getProcessedFrame()
            print("Adding Frame to queue")
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

            if not self.running:
                return

    def terminate(self):
        self.running = False        

def main():
    #Create model
    detector = ColourDetector()
    view = DetectionView()
    #Create controller
    controller = DetectorController(detector,view)
    controller.start()
    #Start the gui
    print("run view")
    view.window.mainloop()
    controller.terminate()

if (__name__ == "__main__"):
     main()