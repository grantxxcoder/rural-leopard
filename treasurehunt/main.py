# main.py

import argparse
from board import Board

def start(board_size, num_jumps, density_walls, mode):
    if (board_size < 5 or num_jumps < 0 or density_walls < 0 or density_walls >= 1 or mode not in [0, 1]):
        print(f"Board size (n) must be greater than 5.")
        print(f"Jump tokens (j) must be greater than 0.")
        print(f"Density of walls (d) must be greater than 0 and less than 1.")
        print(f"Gui (t) must be either 0 or 1.\n")
        exit(0)
    else:
        print(f"Board size: {board_size}")
        print(f"Jump tokens: {num_jumps}")
        print(f"Density of walls: {density_walls}")
        print(f"Mode: {mode}")
        print(f"==================")

    if (mode == 0):
        print(f"Starting terminal game...")
        board = Board(board_size, num_jumps, density_walls)
        board.show_stats()

    else:
        print(f"Starting gui game...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, required=True, help="Board size")
    parser.add_argument("-j", type=int, required=True, help="Number of jump tokens")
    parser.add_argument("-d", type=float, required=True, help="Density of Walls")
    parser.add_argument("-t", type=int, choices=[0, 1], required=True, help="Mode: 1 for terminal, 0 for GUI")

    args = parser.parse_args()
    start(args.n, args.j, args.d, args.t)



if __name__ == "__main__":
    main()
