from threading import Thread
from behavior import Behavior
import time

class TurnBehavior(Behavior):
    running = False
    thread = None

    # Constructor.
    def __init__(self, continue_method, reader):
        super().__init__()
        self.continue_method = continue_method
        self.reader = reader
        self.direction = ''
        self.last_command_deliver = False
        self.power = 40
        self.turn_speed = 20
        self.free_run = 0.6
        self.target_passed = False

    # Start Method.
    def turn_on(self, direction, last_command_deliver=False):
        self.running = True
        self.direction = direction
        self.last_command_deliver = last_command_deliver
        thread = Thread(target=self.turn)
        thread.start()

    # Stop Method.
    def turn_off(self, is_self=False):
        self.left_motor.stop()
        self.right_motor.stop()
        self.running = False
        self.target_passed = False

        if is_self:
            self.continue_method()

    # Turn robot clockwise or counter clockwise
    def turn(self):
        # Free run
        self.left_motor.run_direct(duty_cycle_sp=self.power)
        self.right_motor.run_direct(duty_cycle_sp=self.power)

        if self.last_command_deliver:
            time.sleep(self.free_run + 0.2)

        time.sleep(self.free_run)

        # Initial settings.
        if self.direction is 'ccw':
            self.left_motor.run_direct(duty_cycle_sp=-self.turn_speed)
            self.right_motor.run_direct(duty_cycle_sp=self.turn_speed)
        elif self.direction is 'cw':
            self.left_motor.run_direct(duty_cycle_sp=self.turn_speed)
            self.right_motor.run_direct(duty_cycle_sp=-self.turn_speed)

        min_ref = self.reader.min_ref

        time.sleep(0.7)
        while self.running:
            color_read = self.drive_color_sensor.value()

            if color_read < min_ref + 5:
                self.target_passed = True
                if self.direction is 'cw':
                    self.turn_off(True)
                    return

            if self.target_passed and color_read > min_ref + 10:
                self.turn_off(True)

