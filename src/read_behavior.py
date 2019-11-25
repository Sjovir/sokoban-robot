from threading import Thread
from behavior import Behavior
import time


class ReadBehavior(Behavior):
    running = False
    thread = None

    # Constructor.
    def __init__(self):
        super().__init__()
        self.max_ref = 0
        self.min_ref = 100

    # Start Method.
    def turn_on(self):
        self.running = True
        thread = Thread(target=self.read_colors)
        thread.start()

    # Stop Method.
    def turn_off(self):
        self.running = False

    # Read color Method
    def read_colors(self):
        self.left_motor.run_direct(duty_cycle_sp=30)
        self.right_motor.run_direct(duty_cycle_sp=30)
        while self.running:
            read = self.drive_color_sensor.value()
            if self.max_ref < read:
                self.max_ref = read
            if self.min_ref > read:
                self.min_ref = read

        self.left_motor.stop()
        self.right_motor.stop()
        print('Max:', self.max_ref)
        print('Min:', self.min_ref)
