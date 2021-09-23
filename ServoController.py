from gpiozero import Servo

class ServoController():

    def __init__(self):
        self.xAxisServo = Servo(25)#The x axis servo is connected to GPIO pin 25 on the Raspberry Pi
        self.xAxisServo.mid()
        self.yAxisServo = Servo(8) #The y axis servo is connected to pin 8 on the Raspberry Pi
        self.yAxisServo.mid()
        self.currentXVal = 0
        self.currentYVal = 0
        self.moveAlongX

    def moveAlongY(self, angleVal):
        #Check if the servo value is within 1 and -1
        newValue = self.currentYVal + angleVal
        if newValue < 1 and newValue > -1:
            self.yAxisServo.value = newValue
            self.currentYVal = newValue

    def moveAlongX(self, angleVal):
        #Check if the servo value is within 1 and -1
        newValue = self.currentXVal + angleVal
        if newValue < 1 and newValue > -1:
            self.xAxisServo.value = newValue
            self.currentXVal = newValue