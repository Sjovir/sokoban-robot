import ev3dev.ev3 as ev3
from threading import Thread
from time import sleep
from behavior import Behavior

class DriveBehavior(Behavior):
    running = False
    thread = None

    # Constructor.
    # def __init__(self):


    # Start Method.
    def turn_on(self):
        self.running = True
        thread = Thread(target = self.follow_line)
        thread.start()

    # Stop Method.
    def turn_off(self):
        self.running = False

    # Follow Line.
    def follow_line(self):
        # PID tuning
        Kp = 0.5 # proportional gain
        Ki = 0 # integral gain
        Kd = 0 # derivative gain
        dt = self.navigator.get_dt()

        integral = 0
        previous_error = 0

        # Initial measurement.
        color_data =  self.colorSensor.value()

        while self.running:

            # Calculate steering with PID
            error = color_data - self.limited_color_data(color_data)
            integral += (error * dt)
            derivative = (error - previous_error) / dt

            u = (Kp * error) + (Ki * integral) + (Kd * derivative)

            # Determine right or left navigation
            print("Light: ", self.limited_color_data(color_data))
            if self.navigator.get_speed() + abs(u) > 1000:
                if u >= 0:
                    u = 1000 - self.navigator.get_speed()
                else:
                    u = self.navigator.get_speed() - 1000

            self.navigator.drive(u)

            # Wait dt        
            # sleep(self.navigator.get_dt() / 1000)
            print("u value: ", u)

            # Save error as previous error
            previous_error = error

        self.navigator.stop()

    def limited_color_data(self, target_color):
        color_data = self.colorSensor.value()
        if color_data > target_color + 10: return target_color + 10
        elif color_data < target_color - 10: return target_color - 10
        else: return color_data

    