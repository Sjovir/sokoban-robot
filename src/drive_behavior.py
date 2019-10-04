from threading import Thread
from time import sleep
from behavior import Behavior


class DriveBehavior(Behavior):
    running = False
    thread = None

    # Constructor.
    def __init__(self):
        super().__init__()
        self.color_margin = 10

    # Start Method.
    def turn_on(self):
        self.running = True
        thread = Thread(target=self.follow_line)
        thread.start()

    # Stop Method.
    def turn_off(self):
        self.running = False

    # Follow Line.
    def follow_line(self):
        # PID tuning
        Kp = 1  # proportional gain
        # Ki = 0 # integral gain
        # Kd = 0 # derivative gain
        # dt = self.navigator.get_dt()
        #
        # integral = 0
        # previous_error = 0

        # Initial measurement.
        base_color_data = self.drive_color_sensor.value()
        error = 0

        while self.running:

            # Calculate steering with PID
            drive_color_data = base_color_data - self.get_limited_drive_color_data(base_color_data)
            error = drive_color_data# + error
            # integral += (error * dt)
            # derivative = (error - previous_error) / dt

            turn_regulation = (Kp * error)  # + (Ki * integral) + (Kd * derivative)

            if error > 2:
                speed_regulation = (Kp / error) * 200
            else:
                speed_regulation = 200

            # Determine right or left navigation
            print("Light: ", self.get_limited_drive_color_data(drive_color_data))
            if self.navigator.get_speed() + abs(turn_regulation) > 1000:
                if turn_regulation >= 0:
                    turn_regulation = 1000 - self.navigator.get_speed()
                else:
                    turn_regulation = self.navigator.get_speed() - 1000

            self.navigator.set_speed(speed_regulation)
            self.navigator.drive(turn_regulation)

            # Wait dt
            # sleep(self.navigator.get_dt() / 1000)
            print("Turn value: ", turn_regulation)

            # Save error as previous error
            # previous_error = error

        self.navigator.stop()

    def get_limited_drive_color_data(self, target_color):
        drive_color_data = self.drive_color_sensor.value()
        if drive_color_data > target_color + self.color_margin:
            return target_color + self.color_margin
        elif drive_color_data < target_color - self.color_margin:
            return target_color - self.color_margin
        else:
            return drive_color_data
