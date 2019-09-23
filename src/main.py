import ev3dev.ev3 as ev3
from sys import exit
from drive_behavior import DriveBehavior
from navigator import Navigator
btn = ev3.Button()

driveBehavior = DriveBehavior()

driveBehavior.turn_on()

btn_pressed = false

while not btn_pressed:
    if btn.any():
        btn_pressed = true
    # lightData = ultrasonicSensor.value()
    # print("Distance: ", lightData)

driveBehavior.turn_off()
print('Exit')
exit(0)


