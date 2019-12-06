from threading import Thread
from behavior import Behavior
import time


class DeliverBehavior(Behavior):
    running = False
    thread = None

    # Constructor.
    def __init__(self, continue_method, reader):
        super().__init__()
        self.continue_method = continue_method
        self.reader = reader
        self.power = 40
        self.turn_speed = 20
        self.free_run = 0.5
        self.target_passed = False
        self.intersect_hit = False
        self.next_direction = ''

    # Start Method.
    def turn_on(self, next_direction):
        self.running = True
        thread = Thread(target=self.turn)
        self.next_direction = next_direction
        thread.start()

    # Stop Method.
    def turn_off(self):
        self.running = False

    # Turn robot 180 degrees
    def turn(self):
        # Free run
        self.left_motor.run_direct(duty_cycle_sp=-self.power)
        self.right_motor.run_direct(duty_cycle_sp=-self.power)

        time.sleep(self.free_run)

        # Initial settings.
        if self.next_direction is 'cw':
            self.left_motor.run_direct(duty_cycle_sp=-self.turn_speed)
            self.right_motor.run_direct(duty_cycle_sp=self.turn_speed)
        else:
            self.left_motor.run_direct(duty_cycle_sp=self.turn_speed)
            self.right_motor.run_direct(duty_cycle_sp=-self.turn_speed)

        min_ref = self.reader.min_ref

        time.sleep(1)
        while self.running:
            color_read = self.drive_color_sensor.value()

            if color_read < min_ref + 10:
                if self.next_direction is 'cw':
                    self.stop()
                elif color_read < min_ref + 5:
                    self.target_passed = True

            if self.target_passed and color_read > min_ref + 5:
                self.stop()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
        self.next_direction = ''
        self.target_passed = False
        self.intersect_hit = False
        self.continue_method()
