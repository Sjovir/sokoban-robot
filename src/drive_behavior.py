from threading import Thread, Timer
import time
from behavior import Behavior


class DriveBehavior(Behavior):
    running = False
    thread = None

    # Constructor.
    def __init__(self, next_step, reader):
        super().__init__()
        self.next_step = next_step
        self.reader = reader
        self.power = 40
        self.threshold = 5
        self.target_line_color = -1
        self.intersection_passed = False

    # Start Method.
    def turn_on(self):
        self.running = True
        thread = Thread(target=self.follow_line)
        thread.start()

    # Stop Method.
    def turn_off(self):
        self.running = False

    # Read target line color
    def read_target_line_color(self):
        self.target_line_color = self.drive_color_sensor.value()

    # Follow Line.
    def follow_line(self):
        self.left_motor.run_direct()
        self.right_motor.run_direct()

        self.intersection_passed = False
        t = Timer(0.4, self.pass_intersection)
        t.start()

        # PID tuning
        kp = float(0.65)
        kd = 1
        ki = float(0.02)

        min_ref = self.reader.min_ref
        max_ref = self.reader.max_ref
        self.target_line_color = min_ref + (max_ref - min_ref) / 2
        intersect_min_ref = self.reader.intersect_min_ref

        last_error = error = integral = last_color_read = 0
        while self.running:
            color_read = last_color_read
            try:
                color_read = self.drive_color_sensor.value()
            except ValueError:
                print('Follow line Error:', color_read)

            error = self.target_line_color - (100 * (color_read - min_ref) / (max_ref - min_ref))
            derivative = error - last_error
            last_error = error
            integral = float(0.5) * integral + error
            turn_regulation = (kp * error + kd * derivative + ki * integral) * -1
            last_color_read = color_read

            if turn_regulation >= 0:
                if turn_regulation > 100:
                    right_power = 0
                    left_power = self.power
                else:
                    left_power = self.power
                    right_power = self.power - ((self.power * turn_regulation) / 100)
            else:
                if turn_regulation < -100:
                    left_power = 0
                    right_power = self.power
                else:
                    right_power = self.power
                    left_power = self.power + ((self.power * turn_regulation) / 100)

            # print("Turn reg:", turn_regulation, " color_read: ", color_read, " error: ", error, " derivative: ",
            #       derivative, " lastError: ", last_error, " integral: ", integral)

            self.left_motor.duty_cycle_sp = int(left_power)
            self.right_motor.duty_cycle_sp = int(right_power)

            time.sleep(0.01)

            intersect_read = max_ref
            try:
                intersect_read = self.intersect_color_sensor.value()
            except ValueError:
                print('Intersect Error:', intersect_read)
            if self.intersection_passed and intersect_read < intersect_min_ref + 8 and self.running:
                self.turn_off()
                self.next_step()

        self.left_motor.stop()
        self.right_motor.stop()

    def pass_intersection(self):
        self.intersection_passed = True