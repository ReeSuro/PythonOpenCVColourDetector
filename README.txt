To run the software run the main.py script with python 3

The Colour Detection software requires the following packages to run:
 - Pillow with ImageTk and Image (can be installed with 'sudo apt install python3-pil' and 'sudo apt install python3-pil.imagetk')
 - tkinter (can be installed with 'sudo apt isntall python3.8-tk')
 - opencv (if the program is run with newer versions of opencv the program will throw errors)
 - gpiozero (should be pre-installed on a raspberry pi )
 - numpy
 
 Tips for using the program:
 
   - To highlight a specific colour first set the up HSV values as high as possible and the lower
     HSV values as low as possible. Next, increment/decrement each until only the required colour is highlighted.
   - The colour detection works best in well lit areas.
   - The servo moter pwm lines are connected to GPIO pin 25 for the X axis and GPIO 8 for the Y axis. The servos should not be powered from the raspberry pi directly.
