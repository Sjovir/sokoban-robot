import ev3dev.ev3 as ev3
from sys import exit
from drive import DriveBehavior
from navigator import Navigator
btn = ev3.Button()

motor1 = ev3.LargeMotor('outC')
motor2 = ev3.LargeMotor('outD')

#motor1.run_direct()
#motor2.run_direct()

speed = 50
runTime = 3000
stopLength = 50

colorSensor = ev3.ColorSensor('in1')
#colorSensor.mode = 'COL-COLOR'

ultrasonicSensor = ev3.UltrasonicSensor('in2')
ultrasonicSensor.mode = 'US-DIST-CM'

assert ultrasonicSensor.connected, "UltrasonicSensor is not connected"
assert colorSensor.connected, "ColorSensor is not connected"

lightData = ultrasonicSensor.value()

navigator = Navigator(motor1, motor2, 500, 50, 5, 50)
driveBehavior = DriveBehavior(navigator, colorSensor, 56)

navigator.start()
driveBehavior.turn_On()

while not btn.any():
    lightData = ultrasonicSensor.value()
    print("Distance: ", lightData)

driveBehavior.turn_Off()

# while not btn.any():
#     lightData = ultrasonicSensor.value()
#     colorData = colorSensor.value()

#     if not lightData < stopLength and colorData is not 6:
#         motor1.duty_cycle_sp = speed
#         motor2.duty_cycle_sp = speed
#         print('Distance: ' + str(lightData) + ' - Color: ' + str(colorData))
#     else:
#         motor1.duty_cycle_sp = 0
#         motor2.duty_cycle_sp = 0

#motor1.duty_cycle_sp = 0
#motor2.duty_cycle_sp = 0
print('Exit')
exit(0)


