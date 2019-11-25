import ev3dev.ev3 as ev3
from navigator import Navigator

class Behavior:
    def __init__(self):
        self.speed = 200
        # Sensors
        self.drive_color_sensor = ev3.ColorSensor('in2')
        self.intersect_color_sensor = ev3.ColorSensor('in4')
        self.turn_sensor = ev3.GyroSensor('in1')
        # self.can_dist_sensor = ev3.UltrasonicSensor('in2')
        # Motors
        self.left_motor = ev3.LargeMotor('outA')
        self.right_motor = ev3.LargeMotor('outD')
        # Computations
        self.navigator = Navigator(self.left_motor, self.right_motor, 200, 100, 50)
        # Configs
        # self.can_dist_sensor.mode = 'US-DIST-CM'
        # Checks
        assert self.drive_color_sensor.connected, "Drive sensor is not connected"
        assert self.intersect_color_sensor.connected, "Intersect sensor is not connected"
        assert self.turn_sensor.connected, "Can sensor is not connected"
        # assert self.can_dist_sensor.connected, "Can sensor is not connected"
