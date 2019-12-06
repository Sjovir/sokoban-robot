import ev3dev.ev3 as ev3
left_motor = ev3.LargeMotor('outA')
right_motor = ev3.LargeMotor('outD')
left_motor.stop()
right_motor.stop()