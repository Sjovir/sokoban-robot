import ev3dev.ev3 as ev3
from threading import Thread
from time import sleep

class DriveBehavior:
    behavior = "Drive"
    colorSensor = None
    navigator = None
    colorDark = 0
    colorLight = 0
    colorTarget = 0
    running = False
    thread = None

    # Constructor.
    def __init__(self, navigator, colorSensor, colorDark, colorLight, colorTarget):
        self.colorSensor = colorSensor
        self.navigator = navigator
        self.colorDark = colorDark
        self.colorLight = colorLight
        self.colorTarget = colorTarget

    # Start Method.
    def turn_On(self):
        self.running = True
        thread = Thread(target = self.follow_Line)
        thread.start()

    # Stop Method.
    def turn_Off(self):
        self.running = False

    # Follow Line.
    def follow_Line(self):
        while(self.running):
            colorData =  self.colorSensor.value()
            print("Color: ", colorData)
            if(colorData <= self.colorTarget):
                self.navigator.right()
            elif(colorData >= self.colorTarget):
                self.navigator.left()
            else:
                self.navigator.forward()
        self.navigator.stop()
    