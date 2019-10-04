import ev3dev.ev3 as ev3
from sys import exit
from drive_behavior import DriveBehavior
from intersect_behavior import IntersectBehavior
btn = ev3.Button()

class System:
    def __init__(self):
        self.intersection_count = 0

    def increment_intersection_count(self):
        self.intersection_count += 1


# ***************************
# *****    Main Code    *****
# ***************************
system = System()

drive_behavior = DriveBehavior()
drive_behavior.turn_on()

intersect_behavior = IntersectBehavior(system.increment_intersection_count)
# intersect_behavior.turn_on()

btn_pressed = False

while not btn_pressed:
    if btn.any():
        btn_pressed = True
    # lightData = ultrasonicSensor.value()
    # print("Distance: ", lightData)

drive_behavior.turn_off()
intersect_behavior.turn_off()
print('Exit')
exit(0)


