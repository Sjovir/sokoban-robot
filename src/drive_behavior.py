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
        self.target_line_color = -1

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
        # P tuning
        proportional_turn = 2  # proportional gain
        proportional_speed = self.color_margin - self.color_margin * 0.5

        while self.running:

            # Calculate steering with P
            drive_color_data = self.target_line_color - self.get_limited_drive_color_data(self.target_line_color)
            error = drive_color_data

            turn_regulation = (proportional_turn * error)  # + (Ki * integral) + (Kd * derivative)

            self.navigator.drive(turn_regulation)

            # Lower speed when high turn value
            # if abs(error) > self.color_margin - self.color_margin * 0.5:
            #     speed_regulation = abs(proportional_speed / error) * self.speed
            # else:
            #     speed_regulation = self.speed

            # Determine right or left navigation
            # if self.navigator.get_speed() + abs(turn_regulation) > 1000:
            #     if turn_regulation >= 0:
            #         turn_regulation = 1000 - self.navigator.get_speed()
            #     else:
            #         turn_regulation = self.navigator.get_speed() - 1000

            # if speed_regulation + abs(turn_regulation) > 1000:
            #     if turn_regulation >= 0:
            #         turn_regulation = 1000
            #     else:
            #         turn_regulation = - 1000

            # Navigate
            # self.navigator.set_speed(speed_regulation)

            # if turn_regulation >= 0:
            #     self.navigator.drive_right(turn_regulation)
            # else:
            #     self.navigator.drive_left(turn_regulation)
            # self.navigator.drive(turn_regulation)

            # Prints
            print("Light:", self.drive_color_sensor.value(), "Turn: ", turn_regulation, "Speed:", speed_regulation)

        self.navigator.stop()

    def get_limited_drive_color_data(self, target_color):
        drive_color_data = self.drive_color_sensor.value()
        if drive_color_data > target_color + self.color_margin:
            return target_color + self.color_margin
        elif drive_color_data < target_color - self.color_margin:
            return target_color - self.color_margin
        else:
            return drive_color_data
