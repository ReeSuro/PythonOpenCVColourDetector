from numpy.core.numeric import moveaxis
from gpiozero import Servo

class ServoController():

    def __init__(self):
        self.xAxisServo = Servo(25)
        self.yAxisServo = Servo(8)
        self.currentXVal = 0
        self.currentYVal = 0
        self.moveAlongX

    def moveAlongY(self, angleVal):
        #Check if the servo value is within 1 and -1
        newValue = self.currentYVal + angleVal
        if angleVal < 1 and angleVal > -1:
            self.yAxisServo.value = angleVal
            self.currentYVal = newValue

    def moveAlongX(self, angleVal):
        #Check if the servo value is within 1 and -1
        newValue = self.currentYVal + angleVal
        if angleVal < 1 and angleVal > -1:
            self.xAxisServo.value = angleVal
            self.currentXVal = newValue