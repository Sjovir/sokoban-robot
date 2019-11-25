import ev3dev.ev3 as ev3
from sys import exit
import time
from read_behavior import ReadBehavior
from drive_behavior import DriveBehavior

class System:
    def __init__(self):
        self.step_count = 0
        self.program = []
        self.read_behavior = ReadBehavior()
        self.behaviors = {
            "DRIVE": DriveBehavior(self.next_step, self.read_behavior)
        }

    def load_program(self):
        with open("program.txt", "r", encoding="ISO-8859-1") as program_file:
            for line in program_file:                   # Read every line of config file
                for command in range(0, len(line)):
                    self.program.append(command)

        print('Program:', self.program)

    def init(self):
        self.read_behavior.turn_on()
        time.sleep(3)
        self.read_behavior.turn_off()
        self.behaviors["DRIVE"].turn_on()

    def next_step(self):
        self.step_count += 1
        self.continue_step()

    def continue_step(self):
        last_command = self.program[self.step_count - 1]
        command = self.program[self.step_count]
        next_command = self.program[self.step_count + 1]
        print('Continue - last:', last_command, 'command:', command, 'next:', next_command)
        if command.isUpper() and next_command.isLower():
            self.behaviors["DELIVER"].turn_on()
            return

        direction = self.get_direction(command, last_command)
        print('Direction:', direction)
        if direction == 'ccw':
            pass
        elif direction == 'cw':
            pass
        elif direction == 'forward':
            self.behaviors["DRIVE"].turn_on()
        else:
            pass# Never gonna happen

    def get_direction(self, command, last_command):
        directions = ['u', 'r', 'd', 'l']

        # reverse command if delivery
        if last_command.isUpper():
            last_command = directions[directions.index(last_command.lower()) + 2 % 4]

        command_index = directions.index(command.lower())
        last_command_index = directions.index(last_command.lower())

        if command_index == last_command_index:
            return 'forward'
        elif command_index - 1 % 4 == last_command_index:
            return 'ccw'
        elif command_index + 1 % 4 == last_command_index:
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

read_behavior = ReadBehavior()
drive_behavior = DriveBehavior(read_behavior)

btn_pressed = False

print('System booted')

while not btn_pressed:
    if btn.any():
        btn_pressed = True

read_behavior.turn_on()

time.sleep(3)

read_behavior.turn_off()

time.sleep(5)

drive_behavior.turn_on()

btn_pressed = False

while not btn_pressed:
    if btn.any():
        btn_pressed = True

drive_behavior.turn_off()
# intersect_behavior.turn_off()
print('Exit')
exit(0)


