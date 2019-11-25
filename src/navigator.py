class Navigator:
    def __init__(self, left_motor, right_motor, speed, dt, turn_speed):
        self.speed = speed
        self.dt = dt
        self.turn_speed = turn_speed

        self.left_motor = left_motor
        self.right_motor = right_motor

    def start(self):
        self.left_motor.run_direct()
        self.right_motor.run_direct()
        print('started')
    
    def forward(self):
        self.left_motor.run_timed(time_sp=self.dt, speed_sp=self.speed)
        self.right_motor.run_timed(time_sp=self.dt, speed_sp=self.speed)

    def drive(self, compensate_speed):
        # self.left_motor.run_timed(time_sp=self.dt, speed_sp=self.speed + compensate_speed)
        # self.right_motor.run_timed(time_sp=self.dt, speed_sp=self.speed - compensate_speed)
        left = self.limit_drive(self.speed + compensate_speed)
        right = self.limit_drive(self.speed - compensate_speed)
        self.left_motor.run_forever(speed_sp=left)
        self.right_motor.run_forever(speed_sp=right)
        # print('left:', left, 'right', right)

    def drive_left(self, compensate_speed):
        left = self.limit_drive(self.speed + compensate_speed)
        right = self.limit_drive(self.speed - 2 * compensate_speed)
        # self.left_motor.run_timed(time_sp=self.dt, speed_sp=left)
        # self.right_motor.run_timed(time_sp=self.dt, speed_sp=right)

        self.left_motor.run_forever(speed_sp=left)
        self.right_motor.run_forever(speed_sp=right)
        print("Drive_Left - Compensate:", compensate_speed, "Left:", left, "Right:", right)

    def drive_right(self, compensate_speed):
        left = self.limit_drive(self.speed + 2 * compensate_speed)
        right = self.limit_drive(self.speed - compensate_speed)
        # self.left_motor.run_timed(time_sp=self.dt, speed_sp=left)
        # self.right_motor.run_timed(time_sp=self.dt, speed_sp=right)
        self.left_motor.run_forever(speed_sp=left)
        self.right_motor.run_forever(speed_sp=right)
        print("Drive_Right - Compensate:", compensate_speed, "Left:", left, "Right:", right)
    
    def turn_left(self):
        self.left_motor.run_timed(time_sp=self.dt, speed_sp=-self.turn_speed)
        self.right_motor.run_timed(time_sp=self.dt, speed_sp=self.turn_speed)
    
    def turn_right(self):
        self.left_motor.run_timed(time_sp=self.dt, speed_sp=self.turn_speed)
        self.right_motor.run_timed(time_sp=self.dt, speed_sp=-self.turn_speed)

    def stop(self):
        self.left_motor.duty_cycle_sp = 0
        self.right_motor.duty_cycle_sp = 0
        self.left_motor.stop()
        self.right_motor.stop()

    def set_speed(self, value):
        self.speed = value

    def get_speed(self):
        return self.speed

    def get_dt(self):
        return self.dt   

    def limit_drive(self, value):
        if self.speed + abs(value) > 900:
            if value >= 0:
                return 900
            else:
                return - 900
        else:
            return value