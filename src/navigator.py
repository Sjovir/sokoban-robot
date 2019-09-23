class Navigator:
    def __init__(self, leftMotor, rightMotor, speed, compensateSpeed, turnSpeed):
        self.speed = speed
        self.compensateSpeed = compensateSpeed
        self.turnSpeed = turnSpeed

        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

    def start(self):
        self.leftMotor.run_direct()
        self.rightMotor.run_direct()
    
    def forward(self):
        self.leftMotor.duty_cycle_sp = self.speed
        self.rightMotor.duty_cycle_sp = self.speed

    def left(self):
        self.leftMotor.duty_cycle_sp = self.speed + self.compensateSpeed
        self.rightMotor.duty_cycle_sp = self.speed - self.compensateSpeed

    def right(self):
        self.leftMotor.duty_cycle_sp = self.speed - self.compensateSpeed
        self.rightMotor.duty_cycle_sp = self.speed + self.compensateSpeed
    
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
