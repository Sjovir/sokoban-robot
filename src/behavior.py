import ev3dev.ev3 as ev3
from navigator import Navigator

class Behavior:
    def __init__(self):
        # Sensors
        self.drive_color_sensor = ev3.ColorSensor('in3')
        self.intersect_color_sensor = ev3.ColorSensor('in4')
        # self.can_touch_sensor = ev3.TouchSensor('in2')
        self.can_dist_sensor = ev3.UltrasonicSensor('in2')
        # Motors
        self.left_motor = ev3.LargeMotor('outA')
        self.right_motor = ev3.LargeMotor('outD')
        # Computations
        self.navigator = Navigator(self.left_motor, self.right_motor, 200, 200, 50)
        # Configs
        self.can_dist_sensor.mode = 'US-DIST-CM'
        # Checks
        assert self.drive_color_sensor.connected, "Drive sensor is not connected"
        assert self.intersect_color_sensor.connected, "Intersect sensor is not connected"
        # assert self.can_touch_sensor.connected, "Can sensor is not connected"
        assert self.can_dist_sensor.connected, "Can sensor is not connected"
