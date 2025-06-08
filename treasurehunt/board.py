from enum import Enum
import random

class TileColor(Enum):
    BLUE = 0
    YELLOW = 1
    ORANGE = 2
    RED = 3
    GREEN = 4

class Board:
    def __init__(self, n, jump_tokens, density_walls):
        self.n = n
        self.jump_tokens = jump_tokens
        self.density_walls = density_walls
        self.grid = [[TileColor.BLUE for _ in range(n)] for _ in range(n)]
        self.walls = set()
        self.insert_jump()
        self.insert_walls()
        self.insert_treasure()

    def show_stats(self):
        print(f"Size: {self.n}x{self.n}")
        print(f"Jump Tokens: {self.jump_tokens}")
        print(f"Walls: {len(self.walls)}")
        print("Board Grid:")
        self.print_grid()

    def print_grid(self):
        # Print top border with vertical walls
        top_border = ""
        for j in range(self.n):
            if ('v', 0, j) in self.walls:  # Vertical wall above first row
                top_border += "❚———"
            else:
                top_border += "————"
        top_border += "—"
        print(top_border)
        
        for i in range(self.n):
            # Print row with values and vertical walls
            row_str = ""
            for j in range(self.n):
                if ('v', i, j) in self.walls:  # Vertical wall to the left of cell (i,j)
                    row_str += "❚ " + self.grid[i][j].name[0] + " "
                else:
                    row_str += "| " + self.grid[i][j].name[0] + " "
            row_str += "|"
            print(row_str)
            
            # Print horizontal divider with horizontal walls
            divider = ""
            for j in range(self.n):
                if ('h', i, j) in self.walls:  # Horizontal wall below cell (i,j)
                    divider += "—==="
                else:
                    divider += "————"
            divider += "—"
            print(divider)

    def insert_jump(self):
        for _ in range(0, self.jump_tokens):
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
            while (self.grid[x][y] == TileColor.YELLOW):
                x = random.randint(0, self.n - 1)
                y = random.randint(0, self.n - 1)
            self.colour_in_square(x, y)

    def colour_in_square(self, x, y):
            self.grid[x][y] = TileColor.ORANGE
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    # Wrap around if out of bounds (overflow to opposite edge)
                    nx = nx % self.n
                    ny = ny % self.n
                    if (nx, ny) != (x, y):
                        self.grid[nx][ny] = TileColor.YELLOW

    def insert_walls(self):
        # Calculate number of walls based on density
        num_walls = int(self.n ** 2 * self.density_walls)
        
        # Generate all possible wall positions
        possible_walls = set()
        
        # Horizontal walls (below each cell, except bottom row)
        for i in range(self.n - 1):
            for j in range(self.n):
                possible_walls.add(('h', i, j))
        
        # Vertical walls (to the right of each cell, except rightmost column)
        for i in range(self.n):
            for j in range(self.n - 1):
                possible_walls.add(('v', i, j))
        
        # Randomly select walls from possible positions
        if num_walls > len(possible_walls):
            num_walls = len(possible_walls)
        
        selected_walls = random.sample(list(possible_walls), num_walls)
        self.walls = set(selected_walls)

    def insert_treasure(self):
        x = random.randint(1, self.n - 1)
        y = random.randint(1, self.n - 1)
        while self.grid[x][y] != TileColor.BLUE:
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
        
        self.grid[x][y] = TileColor.GREEN
        
# Example usage:
if __name__ == "__main__":
    board = Board(8, 3, 0.7)
    board.show_stats()