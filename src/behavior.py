import ev3dev.ev3 as ev3
from navigator import Navigator

class Behavior:
    def __init__(self):
        # Sensors
        self.drive_color_sensor = ev3.ColorSensor('in2')
        self.intersect_color_sensor = ev3.ColorSensor('in4')
        # Motors
        self.left_motor = ev3.LargeMotor('outA')
        self.right_motor = ev3.LargeMotor('outD')
        # Checks
        assert self.drive_color_sensor.connected, "Drive sensor is not connected"
        assert self.intersect_color_sensor.connected, "Intersect sensor is not connected"
