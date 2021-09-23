from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import queue
import numpy as np
import time

class DetectionView():

    def __init__(self):

        #Create image queue
        self.imgQueue = queue.Queue(30)

        # Create main window   
        self.window = tk.Tk() 
        self.window.geometry("1100x600")
        self.window.resizable(height = False, width = False)
        self.window.title('Colour Detector')
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.titleLabel = tk.Label(text = "Colour Detector", font=('Arial Bold', 25))
        
        #Create components
        self.videoFrame = ttk.Frame(self.window ,relief=tk.RAISED)
        self.sliderFrame = ttk.Frame(self.window, relief = tk.RAISED)
        self.upperLabelFrame = ttk.Frame(self.sliderFrame)
        self.lowerLabelFrame = ttk.Frame(self.sliderFrame)
        self.settingsFrame = ttk.Frame(self.window)
        self.displaySettingsFrame = ttk.Frame(self.settingsFrame, relief = tk.RAISED)
        self.filterSettingsFrame = ttk.Frame(self.settingsFrame, relief = tk.RAISED)
        self.trackingFrame = ttk.Frame(self.settingsFrame, relief = tk.RAISED)

        self.slider1 = ttk.Scale(self.sliderFrame, from_ = 0, to = 179, orient='horizontal', length=200)
        self.slider2 = ttk.Scale(self.sliderFrame, from_ = 0, to = 255, orient='horizontal', length=200)
        self.slider3 = ttk.Scale(self.sliderFrame, from_ = 0, to = 255, orient='horizontal', length=200)
        self.slider4 = ttk.Scale(self.sliderFrame, from_ = 0, to = 179, orient='horizontal', length=200)
        self.slider5 = ttk.Scale(self.sliderFrame, from_ = 0, to = 255, orient='horizontal', length=200)
        self.slider6 = ttk.Scale(self.sliderFrame, from_ = 0, to = 255, orient='horizontal', length=200)

        #Bind slider events

        self.slider1.bind("<ButtonRelease-1>", self.onSliderReleased)    
        self.slider2.bind("<ButtonRelease-1>", self.onSliderReleased) 
        self.slider3.bind("<ButtonRelease-1>", self.onSliderReleased) 
        self.slider4.bind("<ButtonRelease-1>", self.onSliderReleased) 
        self.slider5.bind("<ButtonRelease-1>", self.onSliderReleased) 
        self.slider6.bind("<ButtonRelease-1>", self.onSliderReleased)

        self.sliderLabel1 = ttk.Label(self.sliderFrame, text='Upper Hue')
        self.sliderLabel2 = ttk.Label(self.sliderFrame, text='Upper Saturation')
        self.sliderLabel3 = ttk.Label(self.sliderFrame, text='Upper Value')
        self.sliderLabel4 = ttk.Label(self.sliderFrame, text='Lower Hue')
        self.sliderLabel5 = ttk.Label(self.sliderFrame, text='Lower Saturation')
        self.sliderLabel6 = ttk.Label(self.sliderFrame, text='Lower Value')

        self.upperBoundLabel = ttk.Label(self.upperLabelFrame, text='Upper HSV Boundary')
        self.lowerBoundLabel = ttk.Label(self.lowerLabelFrame, text='Lower HSV Boundary')

        self.canvas = tk.Canvas(self.videoFrame, width=640, height=480)

        self.lowerBoundPreview = tk.Canvas(self.lowerLabelFrame, width=50, height=50)
        self.upperBoundPreview = tk.Canvas(self.upperLabelFrame, width=50, height=50)

        ##Create an image array based on the hsv slider values
        blankImage = np.zeros((50,50, 3), np.uint8)
        blankImage[:] = (self.slider1.get(), self.slider2.get(), self.slider3.get()) 

        self.upperPreFrame = ImageTk.PhotoImage(image = Image.fromarray(blankImage))
        self.upperBoundPreview.create_image(0,0, image = self.upperPreFrame, anchor = tk.NW)

        blankImage = np.zeros((50,50, 3), np.uint8)
        blankImage[:] = (self.slider4.get(), self.slider5.get(), self.slider6.get()) 

        ##cover the image array to an image and display on the canvas
        self.lowerPreFrame = ImageTk.PhotoImage(image = Image.fromarray(blankImage))
        self.lowerBoundPreview.create_image(0,0, image = self.lowerPreFrame, anchor = tk.NW)

        ##Display settings frame
        self.displaySetting = tk.IntVar()
        self.displaySettingsLabel = ttk.Label(self.displaySettingsFrame, text='Display Settings')
        self.rawRadio = ttk.Radiobutton(self.displaySettingsFrame, text="Raw", value = 0, variable= self.displaySetting)
        self.hsvRadio = ttk.Radiobutton(self.displaySettingsFrame, text="HSV", value = 1, variable= self.displaySetting)
        self.maskRadio = ttk.Radiobutton(self.displaySettingsFrame, text="Mask", value = 2, variable= self.displaySetting)
        self.rawBoundingRadio = ttk.Radiobutton(self.displaySettingsFrame, text="Raw w/ Bounding", value = 3, variable= self.displaySetting)
        self.hsvBoundingRadio = ttk.Radiobutton(self.displaySettingsFrame, text="HSV w/ Bounding", value = 4, variable = self.displaySetting)
        self.maskBoundingRadio = ttk.Radiobutton(self.displaySettingsFrame, text="Mask w/ Bounding", value = 5, variable = self.displaySetting)

        self.rawRadio.bind("<ButtonRelease-1>", self.onDisplayReleased)
        self.hsvRadio.bind("<ButtonRelease-1>", self.onDisplayReleased)
        self.maskRadio.bind("<ButtonRelease-1>", self.onDisplayReleased)
        self.rawBoundingRadio.bind("<ButtonRelease-1>", self.onDisplayReleased)
        self.hsvBoundingRadio.bind("<ButtonRelease-1>", self.onDisplayReleased)
        self.maskBoundingRadio.bind("<ButtonRelease-1>", self.onDisplayReleased)
        ##Filter settings frame
        self.filterSetting = tk.IntVar()
        self.filterSettingsLabel = ttk.Label(self.filterSettingsFrame, text='Filter Settings')
        self.noFilterRadio = ttk.Radiobutton(self.filterSettingsFrame, text="No Filter", value = 0, var = self.filterSetting)
        self.rawFilterRadio = ttk.Radiobutton(self.filterSettingsFrame, text="Image Filter", value = 1, var = self.filterSetting)
        self.rawMaskFilterRadio = ttk.Radiobutton(self.filterSettingsFrame, text="Image & Mask", value = 2, var = self.filterSetting)

        self.noFilterRadio.bind("<ButtonRelease-1>", self.onFilterReleased)
        self.rawFilterRadio.bind("<ButtonRelease-1>", self.onFilterReleased)
        self.rawMaskFilterRadio.bind("<ButtonRelease-1>", self.onFilterReleased)

        self.trackingState = tk.BooleanVar()
        self.trackingLabel = ttk.Label(self.trackingFrame, text='Tracking')
        self.trackingCheck = ttk.Checkbutton(self.trackingFrame, text="Colour Tracking", onvalue=True, offvalue= False, variable=self.trackingState)
        self.trackingCheck.bind("<ButtonRelease-1>", self.onTrackingReleased)
        ####   Arrange window   ####
        self.titleLabel.pack(side = tk.TOP, pady=(20,10))
        self.sliderFrame.pack(side = tk.RIGHT, padx = (20,50), pady = (50,50), anchor=tk.NE)
        self.settingsFrame.pack(side = tk.RIGHT, padx = (0,10), pady = (50,50), anchor = tk.NE)
        self.displaySettingsFrame.pack(pady = (0,50))
        self.filterSettingsFrame.pack(pady = (0,50))
        self.trackingFrame.pack()
        self.videoFrame.pack()
        self.canvas.pack()

        self.upperLabelFrame.pack()
        self.upperBoundLabel.pack()
        self.upperBoundPreview.pack()
        self.sliderLabel1.pack()
        self.slider1.pack()
        self.sliderLabel2.pack()
        self.slider2.pack()
        self.sliderLabel3.pack()
        self.slider3.pack()
        
        self.lowerLabelFrame.pack()
        self.lowerBoundLabel.pack()
        self.lowerBoundPreview.pack()
        self.sliderLabel4.pack()
        self.slider4.pack()
        self.sliderLabel5.pack()
        self.slider5.pack()
        self.sliderLabel6.pack()
        self.slider6.pack()

        self.displaySettingsLabel.pack()
        self.rawRadio.pack(anchor = tk.W)
        self.hsvRadio.pack(anchor = tk.W)
        self.maskRadio.pack(anchor = tk.W)
        self.rawBoundingRadio.pack(anchor = tk.W)
        self.hsvBoundingRadio.pack(anchor = tk.W)
        self.maskBoundingRadio.pack(anchor = tk.W)

        self.filterSettingsLabel.pack()
        self.noFilterRadio.pack(anchor = tk.W)
        self.rawFilterRadio.pack(anchor = tk.W)
        self.rawMaskFilterRadio.pack(anchor = tk.W)

        self.trackingLabel.pack()
        self.trackingCheck.pack(anchor = tk.W)
        #GUI Flags flag
        self.HSVChanged = False
        self.displaySettingChanged = False
        self.filterSettingChanged = False
        self.trackingChanged = False
        self.running = True
        #Set up displaying event
        self.window.after(1, self.updateVideoFeed)

    def updateVideoFeed(self):
        #If there is an available frame in the queue then display on the canvas
        if self.imgQueue.qsize() > 0:
            newFrame = self.imgQueue.get()
            self.videoFrame = ImageTk.PhotoImage(image = Image.fromarray(newFrame))
            self.canvas.create_image(0,0,image = self.videoFrame, anchor = tk.NW)
        if(self.running is True):   
            self.window.after(1, self.updateVideoFeed)    

    def onSliderReleased(self,event):
         ##Create an image array based on the hsv slider values
        blankImage = np.zeros((50, 50, 3), np.uint8)
        blankImage[:] = (self.slider1.get(), self.slider2.get(), self.slider3.get()) 
        blankImage[:,:,0] = (self.slider1.get())
        blankImage[:,:,1] = (self.slider2.get())
        blankImage[:,:,2] = (self.slider3.get()) 

        self.upperPreFrame = ImageTk.PhotoImage(image = Image.fromarray(blankImage, 'HSV'))
        self.upperBoundPreview.create_image(0,0, image = self.upperPreFrame, anchor = tk.NW)

        blankImage = np.zeros((50, 50, 3), np.uint8)
        blankImage[:,:,0] = (self.slider4.get())
        blankImage[:,:,1] = (self.slider5.get())
        blankImage[:,:,2] = (self.slider6.get()) 

         ##cover the image array to an image and displayon the canvas
        self.lowerPreFrame = ImageTk.PhotoImage(image = Image.fromarray(blankImage, 'HSV'))
        self.lowerBoundPreview.create_image(0,0, image = self.lowerPreFrame, anchor = tk.NW)

        self.HSVChanged = True

    def onDisplayReleased(self,event):
        self.displaySettingChanged = True

    def onFilterReleased(self, event):
        self.filterSettingChanged = True   

    def onTrackingReleased(self, event):
        self.trackingChanged = True

    def addFrame(self,frame):
        #Add a new frame to the queue
          if(self.imgQueue.qsize() < 50):
                self.imgQueue.put(frame)
          else:
                self.imgQueue.get()
                self.imgQueue.put(frame)

    def hsvChanged(self):
        return self.HSVChanged

    def getHSVValues(self):
        self.HSVChanged = False
        return np.array([round(self.slider1.get()), round(self.slider2.get()),round(self.slider3.get()),
        round(self.slider4.get()),round(self.slider5.get()),round(self.slider6.get())], np.uint8)

    def dsChanged(self):
        return self.displaySettingChanged

    def fsChanged(self):
        return self.filterSettingChanged

    def trChanged(self):
        return self.trackingChanged

    def getDisplaySetting(self):
        self.displaySettingChanged = False
        return self.displaySetting.get()
    
    def getFilterSetting(self):
        self.filterSettingChanged = False
        return self.filterSetting.get()

    def getTrackingSetting(self):
        self.trackingChanged = False
        return self.trackingState.get()

    def onClosing(self):
        #When the window is closed set a flag and destroy the resource
        self.running = False
        time.sleep(0.5)
        self.window.destroy()
