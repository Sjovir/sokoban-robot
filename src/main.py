import ev3dev.ev3 as ev3
from sys import exit
import time
from drive_behavior import DriveBehavior
from intersect_behavior import IntersectBehavior


class System:
    def __init__(self):
        self.intersection_count = 0
        self.program = {}
        self.behaviors = {
            "DRIVE": DriveBehavior(),
            "INTERSECT": IntersectBehavior(self.increment_intersection_count)
        }

    def increment_intersection_count(self):
        self.intersection_count += 1
        # START BEAHIVORS HEERE
        self.current_behavior = self.program[self.intersection_count]

        # switch (self.current_behavior) {
        #
        # }

    def load_program(self):
        # localDirectory = os.path.dirname(os.path.realpath(__file__))
        # setupFilePath = localDirectory + './config.ini'

        with open("program.txt", "r", encoding="ISO-8859-1") as program_file:
            for line in program_file:                   # Read every line of config file
                key, value = line.strip().split(':')    # Split on delimiter
                self.program[key] = value

    def run_program(self):
        self.behaviors["INTERSECT"].turn_on()
        # while self.program[self.intersection_count] is not "END":
        #    self.program[self.intersection_count].turn_on()

    def end(self):
        self.behaviors["INTERSECT"].turn_off()

# ***************************
# *****    Main Code    *****
# ***************************
# def limit_speed(value):
#     if abs(value) > 900:
#         if value >= 0:
#             return 900
#         else:
#             return - 900
#     else:
#         return value

btn = ev3.Button()
# system = System()
# system.load_program()

drive_behavior = DriveBehavior()

# intersect_behavior = IntersectBehavior(system.increment_intersection_count)
# intersect_behavior.turn_on()

# drive_color_sensor = ev3.ColorSensor('in4')
# left_motor = ev3.LargeMotor('outA')
# right_motor = ev3.LargeMotor('outD')

btn_pressed = False

print('System booted')

while not btn_pressed:
    if btn.any():
        btn_pressed = True

drive_behavior.read_target_line_color()
# target_color = drive_color_sensor.value()
# base_speed = 400
# kp = 2
# ki = 0
# kd = 0
# last_error = 0
# integral = 0
# derivative = 0
#
# kp_speed = .2

time.sleep(3)

drive_behavior.turn_on()

btn_pressed = False

while not btn_pressed:
    if btn.any():
        btn_pressed = True
    # lightData = ultrasonicSensor.value()
    # print("Distance: ", lightData)

# left_motor.stop()
# right_motor.stop()
drive_behavior.turn_off()
# intersect_behavior.turn_off()
print('Exit')
exit(0)


