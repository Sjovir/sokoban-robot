from threading import Thread
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
        self.color_margin = 10
        self.threshold = 5
        self.target_line_color = -1

    # Start Method.
    def turn_on(self):
        self.running = True
        thread = Thread(target=self.follow_line)
        thread.start()
        print('Turn on DriveBehavior')

    # Stop Method.
    def turn_off(self):
        self.running = False
        print('Turn off DriveBehavior')

    # Read target line color
    def read_target_line_color(self):
        self.target_line_color = self.drive_color_sensor.value()

    # Follow Line.
    def follow_line(self):
        self.left_motor.run_direct()
        self.right_motor.run_direct()

        # PID tuning
        kp = float(0.65)
        kd = 1
        ki = float(0.02)

        power = 60
        min_ref = self.reader.min_ref
        max_ref = self.reader.max_ref
        self.target_line_color = min_ref + (max_ref - min_ref) / 2

        last_error = error = integral = 0
        while self.running:
            color_read = self.target_line_color
            try:
                color_read = self.drive_color_sensor.value()
            except ValueError:
                print('Follow line Error:', color_read)
            error = self.target_line_color - (100 * (color_read - min_ref) / (max_ref - min_ref))
            derivative = error - last_error
            last_error = error
            integral = float(0.5) * integral + error
            turn_regulation = (kp * error + kd * derivative + ki * integral) * -1

            if turn_regulation >= 0:
                if turn_regulation > 100:
                    right_power = 0
                    left_power = power
                else:
                    left_power = power
                    right_power = power - ((power * turn_regulation) / 100)
            else:
                if turn_regulation < -100:
                    left_power = 0
                    right_power = power
                else:
                    right_power = power
                    left_power = power + ((power * turn_regulation) / 100)

            print("Turn reg:", turn_regulation, " color_read: ", color_read, " error: ", error, " derivative: ",
                  derivative, " lastError: ", last_error, " integral: ", integral)

            self.left_motor.duty_cycle_sp = int(left_power)
            self.right_motor.duty_cycle_sp = int(right_power)

            time.sleep(0.01)

            intersect_read = max_ref
            try:
                intersect_read = self.intersect_color_sensor.value()
            except ValueError:
                print('Intersect Error:', intersect_read)
            if intersect_read < min_ref + 10 and self.running:
                self.turn_off()
                self.next_step()

        self.left_motor.stop()
        self.right_motor.stop()

    def get_limited_drive_color_data(self, target_color):
        drive_color_data = self.drive_color_sensor.value()
        if drive_color_data > target_color + self.color_margin:
            return target_color + self.color_margin
        elif drive_color_data < target_color - self.color_margin:
            return target_color - self.color_margin
        else:
            return drive_color_data
