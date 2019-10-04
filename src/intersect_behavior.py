from threading import Thread
from behavior import Behavior


class IntersectBehavior(Behavior):
    running = False
    thread = None

    # Constructor.
    def __init__(self, count_method):
        super().__init__()
        self.count_method = count_method
        self.color_margin = 10

    # Start Method.
    def turn_on(self):
        self.running = True
        thread = Thread(target=self.intersect_line)
        thread.start()

    # Stop Method.
    def turn_off(self):
        self.running = False

    # Follow Line.
    def intersect_line(self):
        # Initial measurement.
        base_color_data = self.intersect_color_sensor.value()
        intersection_color = -1

        print('Intersect base:', base_color_data)
        while self.running:
            intersect_color_data = self.intersect_color_sensor.value()
            intersect_color_diff = base_color_data - intersect_color_data

            print('Intersect value:', self.intersect_color_sensor.value(), 'Intersect diff:', intersect_color_diff)

            if intersect_color_data > intersection_color + self.color_margin:
                intersection_color = -1

            if intersection_color is not -1 and intersect_color_diff > self.color_margin:
                self.count_method()
                intersection_color = intersect_color_data


