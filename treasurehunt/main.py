# main.py

import argparse
from board import Board, TileColor
from player import Player

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
        start_terminal_game(board_size, num_jumps, density_walls)

    else:
        print(f"Starting gui game...")

def start_terminal_game(board_size, num_jumps, density_walls):
    board = Board(board_size, num_jumps, density_walls)
    board.show_stats()
    player = Player()
    player_pos = player.get_pos()

    while (board.grid[player_pos[0]][player_pos[1]] != TileColor.GREEN):
        move = input("Your move (w/a/s/d/h/q): ").strip().lower()

        if move == "h":
            print("Move using WASD keys:")
            print("  w - up")
            print("  a - left") 
            print("  s - down")
            print("  d - right")
            print("  h - help")
            print("  q - quit")
            continue

        dx, dy = 0, 0
        if move == "w":
            dx, dy = -1, 0
        elif move == "s":
            dx, dy = 1, 0
        elif move == "a":
            dx, dy = 0, -1
        elif move == "d":
            dx, dy = 0, 1
        elif move == "q":
            exit(1)
        else:
            print("Invalid move. Type 'h' for help.")
            continue

        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy

        # Handle wrapping
        if (new_x < 0):
            new_x = board.n - 1
        elif new_x == board.n:
            new_x = 0
        
        if (new_y < 0):
            new_y = board.n - 1
        elif (new_y == board.n):
            new_y = 0

        new_pos = (new_x, new_y)
        
        # Check if move is blocked by wall
        if not board.has_wall(player_pos, new_pos):
            # Move is not blocked, proceed normally
            move_player(player=player, board=board, new_pos=new_pos)
        elif player.has_jump():
            # Move is blocked but player can jump
            print("Jump over wall!")  
            player.dec_jump()
            move_player(player=player, board=board, new_pos=new_pos)
        else:
            # Move is blocked and no jumps available
            print("Blocked by a wall!")
            continue
        
        # After successful move, check for special tiles
        player_pos = player.get_pos()
        if board.grid[player_pos[0]][player_pos[1]] == TileColor.ORANGE:
            print("Acquired a jump!")
            player.inc_jump()
            board.clear_square(player_pos[0], player_pos[1])

    print("🎉 You found the treasure! 🎉")

def move_player(player, board, new_pos):
    new_x, new_y = new_pos
    player.move(new_x, new_y)
    player_pos = player.get_pos()
    print(f"Moved to {player_pos}. Tile: {board.grid[player_pos[0]][player_pos[1]].name}")
    board.print_grid(player_pos)

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
