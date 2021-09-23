from ServoController import ServoController
from ColourDetectionModel import ColourDetector
from ColourDetectionView import DetectionView
from ColourDetectionController import DetectorController
import time

def main():
    #Create model
    detector = ColourDetector()
    view = DetectionView()
    #Create controller
    servoController = ServoController()
    controller = DetectorController(detector,view, servoController)
    controller.start()
    #Start the gui
    view.window.mainloop()
    time.sleep(2)
    

if (__name__ == "__main__"):
     main()