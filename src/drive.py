import ev3dev.ev3 as ev3
from threading import Thread
from time import sleep

class DriveBehavior:
    colorSensor = None
    navigator = None
    colorTarget = 0
    running = False
    thread = None

    # Constructor.
    def __init__(self, navigator, colorSensor, colorTarget):
        self.colorSensor = colorSensor
        self.navigator = navigator
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
        # PID tuning
        Kp = 1 # proportional gain
        Ki = 0 # integral gain
        Kd = 0 # derivative gain
        dt = 500 # milliseconds
        
        integral = 0
        previous_error = 0

        # Initial measurement.
        colorData =  self.colorSensor.value()

        while(self.running):

            # Calculate steering with PID
            error = colorData - self.colorSensor.value()
            integral += (error * dt)
            derivative = (error - previous_error) / dt

            u = (Kp * error) + (Ki * integral) + (Kd * derivative)

            if self.navigator.getSpeed() + abs(u) > 1000:
                if u >= 0:
                    u = 1000 - self.navigator.getSpeed()
                else:
                    u = self.navigator.getSpeed() - 1000

            print("u value: ", u)

            # Save error as previous error
            previous_error = error

        self.navigator.stop()
    