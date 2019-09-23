class Navigator:
    def __init__(self, leftMotor, rightMotor, speed, dt, turnSpeed):
        self.speed = speed
        self.dt = dt
        self.turnSpeed = turnSpeed

        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

    def start(self):
        self.leftMotor.run_direct()
        self.rightMotor.run_direct()
    
    def forward(self):
    #     self.leftMotor.duty_cycle_sp = self.speed
    #     self.rightMotor.duty_cycle_sp = self.speed
        self.leftMotor.run_timed(self.dt, self.speed)
        self.rightMotor.run_timed(self.dt, self.speed)

    def drive(self, compensateSpeed):
        self.leftMotor.run_timed(time_sp=self.dt, speed_sp=self.speed + compensateSpeed)
        self.rightMotor.run_timed(time_sp=self.dt, speed_sp=self.speed - compensateSpeed)

    def left(self, compensateSpeed):
        # self.leftMotor.duty_cycle_sp = self.speed + self.compensateSpeed
        # self.rightMotor.duty_cycle_sp = self.speed - self.compensateSpeed
        self.leftMotor.run_timed(time_sp=self.dt, speed_sp=self.speed + compensateSpeed)
        self.rightMotor.run_timed(time_sp=self.dt, speed_sp=self.speed - compensateSpeed)
        print("Left: ", self.speed + compensateSpeed)

    def right(self, compensateSpeed):
        # self.leftMotor.duty_cycle_sp = self.speed - self.compensateSpeed
        # self.rightMotor.duty_cycle_sp = self.speed + self.compensateSpeed
        self.leftMotor.run_timed(time_sp=self.dt, speed_sp=self.speed + compensateSpeed)
        self.rightMotor.run_timed(time_sp=self.dt, speed_sp=self.speed - compensateSpeed)
        print("Left: ", self.speed + compensateSpeed)
    
    def turnLeft(self):
        self.leftMotor.duty_cycle_sp = -self.turnSpeed
        self.rightMotor.duty_cycle_sp = self.turnSpeed
    
    def turnRight(self):
        self.leftMotor.duty_cycle_sp = self.turnSpeed
        self.rightMotor.duty_cycle_sp = -self.turnSpeed

    def stop(self):
        self.leftMotor.duty_cycle_sp = 0
        self.rightMotor.duty_cycle_sp = 0

    def getSpeed(self):
        return self.speed

    def getDt(self):
        return self.dt   
