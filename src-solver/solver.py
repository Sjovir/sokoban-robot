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

    def solve_puzzle(self):
        # print('Solving...', self.map)

        paths = [[self.__get_player_position()]]
        add_state(self.__get_player_position(), self.__get_jewels_positions())

        while True:
            for path_index in range(len(paths) - 1, -1, -1):
                path = paths[path_index]
                self.__update_map(path)

                player_pos = path[-1]
                moves = self.__get_walkable_directions(player_pos)

                # print('** checking:', path, '** Valid moves:', moves, ' ** jewel:')
                for index in range(len(moves) - 1, -1, -1):
                    self.__update_map(path)

                    new_pos = moves[index]
                    self.__move_player(player_pos, new_pos)

                    jewel_pos = self.__get_jewels_positions()

                    if not is_state_new(new_pos, jewel_pos) or self.__check_deadlock(jewel_pos):
                        if index is 0:
                            del paths[path_index]
                        continue

                    add_state(new_pos, jewel_pos)

                    if index is 0:
                        path.append(new_pos)

                        if self.__check_win_condition(jewel_pos):
                            return path

                        paths[path_index] = path
                    else:
                        new_path = path.copy()
                        new_path.append(new_pos)

                        if self.__check_win_condition(jewel_pos):
                            return new_path

                        paths.append(new_path)
                    # self.__print_map()

            # print('paths:', paths)
            print('paths:', len(paths), 'length:', len(paths[0]))
            print()
            # time.sleep(.1)

    def __check_deadlock(self, jewel_pos):
        for jewel_index in jewel_pos:
            if jewel_index in self.goal_indeces:
                continue

            # Jewels in corner
            if self.map[self.__above(jewel_index)] is 'X':
                if self.map[self.__left(jewel_index)] is 'X' or self.map[self.__right(jewel_index)] is 'X':
                    # self.__print_map()
                    return True
            if self.map[self.__below(jewel_index)] is 'X':
                if self.map[self.__left(jewel_index)] is 'X' or self.map[self.__right(jewel_index)] is 'X':
                    # self.__print_map()
                    return True
            if self.map[self.__left(jewel_index)] is 'X':
                if self.map[self.__above(jewel_index)] is 'X' or self.map[self.__below(jewel_index)] is 'X':
                    # self.__print_map()
                    return True
            if self.map[self.__right(jewel_index)] is 'X':
                if self.map[self.__above(jewel_index)] is 'X' or self.map[self.__below(jewel_index)] is 'X':
                    # self.__print_map()
                    return True

            # Jewels next to each other next to walls
            if self.map[self.__above(jewel_index)] is 'X':
                left_index = self.__left(jewel_index)
                right_index = self.__right(jewel_index)
                if self.map[left_index] is 'J' and (self.map[self.__above(left_index)] is 'X' or self.map[self.__below(left_index)] is 'X'):
                    # self.__print_map()
                    return True
                elif self.map[right_index] is 'J' and (self.map[self.__above(right_index)] is 'X' or self.map[self.__below(left_index)] is 'X'):
                    # self.__print_map()
                    return True
            if self.map[self.__below(jewel_index)] is 'X':
                left_index = self.__left(jewel_index)
                right_index = self.__right(jewel_index)
                if self.map[left_index] is 'J' and (self.map[self.__above(left_index)] is 'X' or self.map[self.__below(left_index)] is 'X'):
                    # self.__print_map()
                    return True
                elif self.map[right_index] is 'J' and (self.map[self.__above(right_index)] is 'X' or self.map[self.__below(left_index)] is 'X'):
                    # self.__print_map()
                    return True
            if self.map[self.__left(jewel_index)] is 'X':
                above_index = self.__above(jewel_index)
                below_index = self.__below(jewel_index)
                if self.map[above_index] is 'J' and (self.map[self.__left(above_index)] is 'X' or self.map[self.__right(above_index)] is 'X'):
                    # self.__print_map()
                    return True
                elif self.map[below_index] is 'J' and (self.map[self.__left(below_index)] is 'X' or self.map[self.__right(below_index)] is 'X'):
                    # self.__print_map()
                    return True
            if self.map[self.__right(jewel_index)] is 'X':
                above_index = self.__above(jewel_index)
                below_index = self.__below(jewel_index)
                if self.map[above_index] is 'J' and (self.map[self.__left(above_index)] is 'X' or self.map[self.__right(above_index)] is 'X'):
                    # self.__print_map()
                    return True
                elif self.map[below_index] is 'J' and (self.map[self.__left(below_index)] is 'X' or self.map[self.__right(above_index)] is 'X'):
                    # self.__print_map()
                    return True

        return False

    def __check_win_condition(self, jewel_indices):
        for jewel in jewel_indices:
            if jewel not in self.goal_indeces:
                return False

        return True

    def __update_map(self, moves, index=1):
        self.map = self.original_map.copy()
        while index < len(moves):
            destination_tile = moves[index]
            starting_tile = moves[index - 1]

            self.__move_player(starting_tile, destination_tile)
            index += 1

    def __move_player(self, starting_tile, destination_tile):
        if self.map[destination_tile] is 'J':
            diff = destination_tile - starting_tile
            direction = ''

            if diff == - self.width:
                direction = 'up'
            elif diff == self.width:
                direction = 'down'
            elif diff == - 1:
                direction = 'left'
            elif diff == 1:
                direction = 'right'

            tile_index = self.__get_tile(direction, destination_tile)

            self.map[tile_index] = 'J'

        self.map[destination_tile] = 'M'

        original_tile = self.original_map[starting_tile]
        self.map[starting_tile] = original_tile if not original_tile in ['M', 'J'] else '.'

    def __get_player_position(self):
        return self.map.index('M')

    def __get_jewels_positions(self):
        return [index for index, condition in enumerate(self.map) if condition == 'J']

    def __get_walkable_directions(self, index):
        up = self.__get_tile('up', index, ['X'])
        down = self.__get_tile('down', index, ['X'])
        left = self.__get_tile('left', index, ['X'])
        right = self.__get_tile('right', index, ['X'])

        up = self.__validate_jewel_move('up', up)
        down = self.__validate_jewel_move('down', down)
        left = self.__validate_jewel_move('left', left)
        right = self.__validate_jewel_move('right', right)

        directions = []

        if up is not None:
            directions.append(up)
        if down is not None:
            directions.append(down)
        if left is not None:
            directions.append(left)
        if right is not None:
            directions.append(right)

        return directions

    def __validate_jewel_move(self, relation, index) -> Optional[int]:
        if index is not None and self.map[index] is 'J' and self.__get_tile(relation, index, ['X', 'J']) is None:
            return None

        return index

    def __get_tile(self, relation, index, remove_conditions=[]):
        try:
            if relation == 'up':
                tile_index = self.__above(index)
            elif relation == 'down':
                tile_index = self.__below(index)
            elif relation == 'left':
                tile_index = self.__left(index)
            elif relation == 'right':
                tile_index = self.__right(index)
            else:
                tile_index = -1
                print('Unknown relation')
                raise Exception
        except Exception:
            return None

        if self.map[tile_index] in remove_conditions:
            return None
        else:
            return tile_index

    def __above(self, index):
        tile_index = index - self.width
        if tile_index < 0:
            raise Exception
        return tile_index

    def __below(self, index):
        tile_index = index + self.width
        return tile_index

    def __left(self, index):
        tile_index = index - 1
        if tile_index % self.width == self.width - 1:
            raise Exception
        return tile_index

    def __right(self, index):
        tile_index = index + 1
        if tile_index % self.width == 0:
            raise Exception
        return tile_index

    def __print_map(self):
        print('** Map **')
        for index_y in range(0, self.width):
            line = ''
            for index_x in range(0, self.height):
                tile_index = index_y * self.height + index_x
                line += self.map[tile_index]

            print(line)
        pass