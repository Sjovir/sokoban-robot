from state import states, add_state, is_state_new, state_to_string
from typing import Optional
import time

class Solver:
    def __init__(self):
        self.map = []
        self.original_map = []
        self.goal_indeces = -1
        self.width = -1
        self.height = -1
        self.paths = []

    def load_map(self, map, width, height):
        self.width = width
        self.height = height
        with open(map, "r", encoding='ISO-8859-1') as map_file:
            for line in map_file:                   # Read every line of config file
                for tile in line:                   # Read every character in lines as a tile
                    if tile is not '\n':            # Remove newline characters
                        self.original_map.append(tile)       # Add tile to map

        self.map = self.original_map.copy()
        self.goal_indeces = [index for index, condition in enumerate(self.original_map) if condition == 'G']

def solve_puzzle_threaded(self):
    # print('Solving...', self.map)

    self.paths = [[self.__get_player_position()]]
    add_state(self.__get_player_position(), self.__get_jewels_positions())

    while True:
        for path_index in range(len(paths) - 1, -1, -1):
            path = paths[path_index]
            self.__update_map(path)

            player_pos = path[-1]
            moves = self.__get_walkable_directions(player_pos)

            # print('** checking:', path, '** Valid moves:', moves, ' ** jewel:')
            for index in range(len(moves) - 1, -1, -1):
                pass

        # print('paths:', paths)
        print('paths:', len(self.paths), 'length:', len(self.paths[0]))
        print()
        # time.sleep(.1)

def solve_move_threaded(self, path_index, path, player_pos, new_pos, move_index, map, lock):
    self.__update_map(path)

    self.__move_player(player_pos, new_pos)

    jewel_pos = self.__get_jewels_positions()

    if not is_state_new(new_pos, jewel_pos) or self.__check_deadlock(jewel_pos):
        if move_index is 0:
            del self.paths[path_index]
        return []

    add_state(new_pos, jewel_pos)

    if move_index is 0:
        path.append(new_pos)

        if self.__check_win_condition(jewel_pos):
            return path

        self.paths[path_index] = path
    else:
        new_path = path.copy()
        new_path.append(new_pos)

        if self.__check_win_condition(jewel_pos):
            return new_path

        self.paths.append(new_path)
    # self.__print_map()

    return []
