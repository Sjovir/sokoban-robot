from threading import Thread
from behavior import Behavior
import time


class ReadBehavior(Behavior):
    running = False
    thread = None

    # Constructor.
    def __init__(self):
        super().__init__()
        self.min_ref = 100
        self.max_ref = 0
        self.intersect_min_ref = 100
        self.intersect_max_ref = 0

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

            intersect_read = self.intersect_color_sensor.value()
            if self.intersect_max_ref < intersect_read:
                self.intersect_max_ref = intersect_read
            if self.intersect_min_ref > intersect_read:
                self.intersect_min_ref = intersect_read
            print('1:', read, '2:', intersect_read)

        self.left_motor.stop()
        self.right_motor.stop()
        print('Min:', self.min_ref)
        print('Max:', self.max_ref)
        print('Intersect Min:', self.intersect_min_ref)
        print('Intersect Max:', self.intersect_max_ref)
