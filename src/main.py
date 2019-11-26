import ev3dev.ev3 as ev3
from sys import exit
import time
from read_behavior import ReadBehavior
from drive_behavior import DriveBehavior
from turn_behavior import TurnBehavior
from deliver_behavior import DeliverBehavior


class System:
    def __init__(self):
        self.step_count = 0
        self.program = []
        self.deliver = False
        self.move_to_jewel_tile = False
        self.read_behavior = ReadBehavior()
        self.behaviors = {
            "DRIVE": DriveBehavior(self.next_step, self.read_behavior),
            "TURN": TurnBehavior(self.continue_step, self.read_behavior),
            "DELIVER": DeliverBehavior(self.continue_step, self.read_behavior)
        }

    def load_program(self):
        with open("test_program.txt", "r", encoding="ISO-8859-1") as program_file:
            for line in program_file:  # Read every line of config file
                for index in range(0, len(line)):
                    self.program.append(line[index])
        self.program = self.program[0:-1]
        print('Program:', self.program)

    def init(self):
        btn_pressed = False

        print('System booted')

        while not btn_pressed:
            if btn.any():
                btn_pressed = True

        self.read_behavior.turn_on()
        time.sleep(3)
        self.read_behavior.turn_off()
        time.sleep(5)
        self.behaviors["DRIVE"].turn_on()

        btn_pressed = False

        while not btn_pressed:
            if btn.any():
                btn_pressed = True

        self.behaviors["TURN"].turn_off()
        self.behaviors["DELIVER"].turn_off()
        self.behaviors["DRIVE"].turn_off()

        left_motor = ev3.LargeMotor('outA')
        right_motor = ev3.LargeMotor('outD')

        left_motor.stop()
        right_motor.stop()

        print('Exit')
        exit(0)

    def next_step(self):
        if self.deliver:
            if self.move_to_jewel_tile:
                command = self.program[self.step_count]
                next_command = 'End'
                if len(self.program) > self.step_count + 1:
                    next_command = self.program[self.step_count + 1]
                direction = self.get_direction(next_command, command)
                self.behaviors["DELIVER"].turn_on(direction)
                return
            else:
                self.move_to_jewel_tile = True
                self.continue_step()
                return

        self.step_count += 1

        if len(self.program) == self.step_count:
            self.end()
            return

        last_command = self.program[self.step_count - 1]
        command = self.program[self.step_count]
        next_command = 'End'
        if len(self.program) > self.step_count + 1:
            next_command = self.program[self.step_count + 1]

        print('Continue - last:', last_command, 'command:', command, 'next:', next_command)
        if command.isupper() and next_command.islower():
            self.deliver = True
            print("Deliver set")

        direction = self.get_direction(command, last_command)
        print('Direction:', direction)
        if direction == 'ccw' or direction == 'cw':
            self.behaviors["TURN"].turn_on(direction, last_command.isupper())
        elif direction == 'forward':
            self.behaviors["DRIVE"].turn_on()
        else:
            pass  # Never gonna happen

    def continue_step(self):
        if self.deliver and self.behaviors["DELIVER"].running:
            self.deliver = False
            self.move_to_jewel_tile = False
            self.behaviors["DELIVER"].turn_off()

        self.behaviors["DRIVE"].turn_on()
        print('Continue step')

    def get_direction(self, command, last_command):
        directions = ['u', 'r', 'd', 'l']

        # reverse command if delivery
        if last_command.isupper():
            last_command = directions[(directions.index(last_command.lower()) + 2) % 4]

        command_index = directions.index(command.lower())
        last_command_index = directions.index(last_command.lower())
        print('index:', command_index, 'last index:', last_command_index)
        print('ccw:', (last_command_index - 1) % 4)
        print('cw:', (last_command_index + 1) % 4)
        if last_command_index == command_index:
            return 'forward'
        elif (last_command_index - 1) % 4 == command_index:
            return 'ccw'
        elif (last_command_index + 1) % 4 == command_index:
            return 'cw'
        else:
            return 'back'

    def end(self):
        # self.behaviors["INTERSECT"].turn_off()
        pass


# ***************************
# *****    Main Code    *****
# ***************************

btn = ev3.Button()
system = System()
system.load_program()
system.init()
# system.read_colors()
#
# read_behavior = ReadBehavior()
# drive_behavior = DriveBehavior(system.next_step, read_behavior)
#
# btn_pressed = False
#
# print('System booted')
#
# while not btn_pressed:
#     if btn.any():
#         btn_pressed = True
#
# read_behavior.turn_on()
#
# time.sleep(3)
#
# read_behavior.turn_off()
#
# time.sleep(5)
#
# drive_behavior.turn_on()
#
# btn_pressed = False
#
# while not btn_pressed:
#     if btn.any():
#         btn_pressed = True
#
# drive_behavior.turn_off()
# # intersect_behavior.turn_off()
# print('Exit')
# exit(0)
