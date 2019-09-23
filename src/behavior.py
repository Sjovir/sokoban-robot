import ev3dev.ev3 as ev3
from navigator import Navigator

class Behavior:
    def __init__(self):
        self.colorSensor = ev3.ColorSensor('in1')
        self.motor1 = ev3.LargeMotor('outC')
        self.motor2 = ev3.LargeMotor('outD')
        self.navigator = Navigator(self.motor1, self.motor2, 200, 200, 50)
        self.ultrasonicSensor = ev3.UltrasonicSensor('in2')
        self.ultrasonicSensor.mode = 'US-DIST-CM'

        assert self.ultrasonicSensor.connected, "UltrasonicSensor is not connected"
        assert self.colorSensor.connected, "ColorSensor is not connected"
