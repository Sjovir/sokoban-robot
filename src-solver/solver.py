from state import states, add_state, is_state_new, state_to_string
import time

class Solver:
    def __init__(self):
        self.map = []
        self.original_map = []
        self.goal_index = -1
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
        self.goal_index = self.original_map.index('G')

    def solve_puzzle(self):
        print('Solving...', self.map)

        paths = [[self.__get_player_position()]]
        add_state(self.__get_player_position(), self.__get_jewels_positions())

        while True:
            for path_index in range(len(paths) - 1, -1, -1):
                path = paths[path_index]
                print('** checking:', path, '**')
                self.__update_map(path)

                player_pos = path[-1]
                moves = self.__get_walkable_directions(player_pos)
                print(moves)
                if len(moves) > 1:
                    for index in range(len(moves) - 1, -1, -1):
                        self.__update_map(path)
                        new_pos = moves[index]

                        if index is 0:
                            path.append(new_pos)
                            winner_path, new_state = self.__check_new_path(path)
                            if len(winner_path) is not 0:
                                return winner_path

                            if not new_state:
                                print('removed', path[-1], 'path', path)
                                path = path[:-1]

                            paths[path_index] = path
                            print('path', path)
                        else:
                            new_path = path.copy()
                            current_pos = path[-1]
                            self.__move_player(current_pos, new_pos)

                            jewel_pos = self.__get_jewels_positions()

                            if not is_state_new(new_pos, jewel_pos):
                                continue

                            add_state(new_pos, jewel_pos)
                            new_path.append(new_pos)

                            if self.__check_win_condition(jewel_pos):
                                return path

                            paths.append(new_path)
                            print('path', new_path)

                else:
                    current_pos = path[-1]
                    new_pos = moves[0]
                    self.__move_player(current_pos, new_pos)

                    jewel_pos = self.__get_jewels_positions()

                    if not is_state_new(new_pos, jewel_pos):
                        continue

                    add_state(new_pos, jewel_pos)
                    path.append(new_pos)

                    if self.__check_win_condition(jewel_pos):
                        return path

                    paths[path_index] = path
                    print('path', path)

            print('paths:', paths)
            time.sleep(1)

    def __check_new_path(self, path):
        new_pos = path[-1]
        # self.__update_map(path, len(path) - 1)
        self.__move_player(path[-1], new_pos)

        jewels_pos = self.__get_jewels_positions()

        if self.__check_win_condition(jewels_pos):
            return path

        new_state = is_state_new(new_pos, jewels_pos)
        if new_state:
            add_state(new_pos, jewels_pos)

        return [], new_state

    def __check_deadlock(self):
        pass

    def __check_win_condition(self, jewel_index):
        # jewel_index = self.map.index('J')
        # goal_index = self.original_map.index('G')
        if jewel_index is self.goal_index:
            return True
        else:
            return False

    def __update_map(self, moves, index=1):
        self.map = self.original_map.copy()
        while index < len(moves):
            destination_tile = moves[index]
            starting_tile = moves[index - 1]

            self.__move_player(starting_tile, destination_tile)
            index += 1

    def __move_player(self, starting_tile, destination_tile):
        if destination_tile is 'J':
            diff = destination_tile - starting_tile
            direction = ''

            if diff is - self.width:
                direction = 'up'
            elif diff is self.width:
                direction = 'down'
            elif diff is - 1:
                direction = 'left'
            elif diff is 1:
                direction = 'right'

            tile_index = self.__get_tile(direction, destination_tile)

            self.map[tile_index] = 'J'

        self.map[destination_tile] = 'M'
        self.map[starting_tile] = self.original_map[starting_tile]

    def __get_player_position(self):
        return self.map.index('M')

    def __get_jewels_positions(self):
        return [index for index, condition in enumerate(self.map) if condition == 'J']

    def __get_walkable_directions(self, index):
        up = self.__get_tile('up', index, ['X'])
        down = self.__get_tile('down', index, ['X'])
        left = self.__get_tile('left', index, ['X'])
        right = self.__get_tile('right', index, ['X'])

        if up is not None and self.map[up] is 'J' and self.__get_tile('up', up, ['X', 'J']) is None:
            up = None
        if down is not None and self.map[down] is 'J' and self.__get_tile('down', down, ['X', 'J']) is None:
            down = None
        if left is not None and self.map[left] is 'J' and self.__get_tile('left', left, ['X', 'J']) is None:
            left = None
        if right is not None and self.map[right] is 'J' and self.__get_tile('right', right, ['X', 'J']) is None:
            right = None

        directions = []

        if up is not None:
            directions.append(up)
        if down is not None:
            directions.append(down)
        if left is not None:
            directions.append(left)
        if right is not None:
            directions.append(right)

        # directions = [up, down, left, right]

        # for direction in directions:
        #     if direction is None or direction is 'X':
        #         directions.remove(direction)

        return directions

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
        except:
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