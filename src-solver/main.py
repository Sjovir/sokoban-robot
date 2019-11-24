from solver import Solver
from state import State
import sys

if __name__ == '__main__':
    solver = Solver()
    # solver.load_map('map.txt', 8, 8)
    # solver.load_map('comp_2018.txt', 7, 12)
    solver.load_map('comp_2019.txt', 12, 7)
    winner_path = solver.solve_puzzle()
    winner_moves = solver.get_moves_from_path(winner_path)

    print("Winner path:", winner_path)
    print()
    print('Winner Moves:', winner_moves)
