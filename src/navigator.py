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
    
    def forward(self):
        self.left_motor.run_timed(time_sp=self.dt, speed_sp=self.speed)
        self.right_motor.run_timed(time_sp=self.dt, speed_sp=self.speed)

    def drive(self, compensate_speed):
        self.left_motor.run_timed(time_sp=self.dt, speed_sp=self.speed + compensate_speed)
        self.right_motor.run_timed(time_sp=self.dt, speed_sp=self.speed - compensate_speed)
    
    def turn_left(self):
        self.left_motor.run_timed(time_sp=self.dt, speed_sp=-self.turn_speed)
        self.right_motor.run_timed(time_sp=self.dt, speed_sp=self.turn_speed)
    
    def turn_right(self):
        self.left_motor.run_timed(time_sp=self.dt, speed_sp=self.turn_speed)
        self.right_motor.run_timed(time_sp=self.dt, speed_sp=-self.turn_speed)

    def stop(self):
        self.left_motor.duty_cycle_sp = 0
        self.right_motor.duty_cycle_sp = 0

    def set_speed(self, value):
        self.speed = value

    def get_speed(self):
        return self.speed

    def get_dt(self):
        return self.dt   
