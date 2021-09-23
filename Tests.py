from ColourDetectionModel import ColourDetector
from ServoController import ServoController
import cv2
import numpy as np
import time

cd = ColourDetector()
srvController = ServoController()
#Test if the video source is available
def cameraInitTest():
    ##Testing Camera state
    print('Testing camera state')
    if cd.cam.isOpened() is False:
        return False
    return True

def imageColourDetectionTest():
    print('Testing Colour Detection')
    cd.setDisplaySetting(3)
    ##Test Purple Colours
    cd.setUpperHSV(np.array([179,255,255], np.uint8))
    cd.setLowerHSV(np.array([130,50,50], np.uint8))
    _, image = cd.getProcessedFrame('testImage.png')
    cv2.imshow('image', image)
    cv2.imwrite('purpleTestResult.png', image)
    
    ##Test blue colours
    cd.setUpperHSV(np.array([120,255,255], np.uint8))
    cd.setLowerHSV(np.array([80,50,50], np.uint8))
    _, image2 = cd.getProcessedFrame('testImage.png')
    cv2.imshow('image2', image2)
    cv2.imwrite('blueTestResult.png', image2)
    
    #Red test results
    cd.setUpperHSV(np.array([40,255,255], np.uint8))
    cd.setLowerHSV(np.array([0,50,50], np.uint8))
    _, image3 = cd.getProcessedFrame('testImage.png')
    cv2.imshow('image3', image3)
    cv2.imwrite('redTestResult.png', image3)
    cv2.waitKey(0)
    
def servoMotorTest():
    ##Testing the xAxis servo
    print('Testing the X axis servo:')
    print('Moving Min...')
    srvController.xAxisServo.min()
    time.sleep(1)
    print('Moving Max...')
    srvController.xAxisServo.max()
    time.sleep(1)
    print('Moving Min...')
    srvController.xAxisServo.min()
    time.sleep(1)
    
    ##Testing the xAxis servo
    print('Testing the Y axis servo:')
    print('Moving Min...')
    srvController.yAxisServo.min()
    time.sleep(1)
    print('Moving Max...')
    srvController.yAxisServo.max()
    time.sleep(1)
    print('Moving Min...')
    srvController.yAxisServo.min()
    time.sleep(1)

def servoMotorIncrementTest():
    ##Testing incrementing the servo angle
    print('Testing servo Y incrementing...')
    for i in range(100):
        srvController.moveAlongY(0.01)
        time.sleep(0.1)
    for j in range(100):
        srvController.moveAlongY(-0.01)
        time.sleep(0.1)
    print('Testing servo X incrementing...')   
    for i in range(100):
        srvController.moveAlongX(0.01)
        time.sleep(0.1)
    for j in range(100):
        srvController.moveAlongX(-0.01)
        time.sleep(0.1)
    
def runTests():
    result = cameraInitTest()
    if result is True:
        print ('Camera connected successfully')
    else:
        print ('Camera connection failed')    
    
    imageColourDetectionTest()
    servoMotorTest()
    servoMotorIncrementTest()
    print('Tests Complete')
    
runTests() 