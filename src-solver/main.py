from solver import Solver
from state import State
import sys

if __name__ == '__main__':
    solver = Solver()
    # solver.load_map('map.txt', 8, 8)
    solver.load_map('comp_2018.txt', 7, 12)
    winner_path = solver.solve_puzzle()

    print("Winner Path:", winner_path)
