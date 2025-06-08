# gui_game.py

import tkinter as tk
from tkinter import messagebox
from board import Board, TileColor
from player import Player

class MazeGameGUI:
    def __init__(self, board_size, num_jumps, density_walls):
        self.board = Board(board_size, num_jumps, density_walls)
        self.player = Player()
        self.player_pos = self.player.get_pos()
        
        # GUI setup
        self.root = tk.Tk()
        self.root.title("Maze Game")
        self.root.resizable(False, False)
        
        # Colors for tiles
        self.colors = {
            TileColor.BLUE: "#4A90E2",
            TileColor.YELLOW: "#F5D547", 
            TileColor.ORANGE: "#FF8C42",
            TileColor.RED: "#E74C3C",
            TileColor.GREEN: "#2ECC71"
        }
        
        # Calculate cell size based on board size
        self.cell_size = max(40, 400 // board_size)
        
        self.setup_ui()
        self.draw_board()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
    def setup_ui(self):
        # Info panel
        info_frame = tk.Frame(self.root, bg="#34495E", padx=10, pady=10)
        info_frame.pack(fill=tk.X)
        
        # Stats labels
        self.stats_label = tk.Label(
            info_frame, 
            text=f"Board: {self.board.n}x{self.board.n} | Jumps: {self.player.jump_tokens} | Position: {self.player_pos}",
            bg="#34495E", 
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.stats_label.pack()
        
        # Instructions
        instructions = tk.Label(
            info_frame,
            text="Use WASD or Arrow Keys to move | Collect orange tokens for jumps | Find the green treasure!",
            bg="#34495E",
            fg="#BDC3C7",
            font=("Arial", 10)
        )
        instructions.pack()
        
        # Canvas for the game board
        canvas_width = self.board.n * self.cell_size + 1
        canvas_height = self.board.n * self.cell_size + 1
        
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg="white",
            highlightthickness=1,
            highlightbackground="#34495E"
        )
        self.canvas.pack(padx=20, pady=20)
        
    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw grid cells
        for i in range(self.board.n):
            for j in range(self.board.n):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Get tile color
                tile_color = self.colors[self.board.grid[i][j]]
                
                # Draw cell
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=tile_color,
                    outline="#2C3E50",
                    width=1
                )
                
                # Draw player
                if (i, j) == self.player_pos:
                    center_x = x1 + self.cell_size // 2
                    center_y = y1 + self.cell_size // 2
                    radius = self.cell_size // 3
                    
                    self.canvas.create_oval(
                        center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        fill="#8E44AD", outline="#6C3483", width=3
                    )
                    
                    # Player symbol
                    self.canvas.create_text(
                        center_x, center_y,
                        text="P",
                        fill="white",
                        font=("Arial", max(8, self.cell_size // 4), "bold")
                    )
        
        # Draw walls
        self.draw_walls()
        
    def draw_walls(self):
        wall_width = 4
        
        for wall in self.board.walls:
            wall_type, row, col = wall
            
            if wall_type == 'h':  # Horizontal wall
                # Wall below cell (row, col)
                x1 = col * self.cell_size
                y1 = (row + 1) * self.cell_size - wall_width // 2
                x2 = x1 + self.cell_size
                y2 = y1 + wall_width
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="#C0392B", outline="#A93226", width=1
                )
                
            elif wall_type == 'v':  # Vertical wall
                # Wall to the left of cell (row, col)
                x1 = col * self.cell_size - wall_width // 2
                y1 = row * self.cell_size
                x2 = x1 + wall_width
                y2 = y1 + self.cell_size
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="#C0392B", outline="#A93226", width=1
                )
    
    def on_key_press(self, event):
        # Handle key presses
        key = event.keysym.lower()
        
        dx, dy = 0, 0
        if key in ['w', 'up']:
            dx, dy = -1, 0
        elif key in ['s', 'down']:
            dx, dy = 1, 0
        elif key in ['a', 'left']:
            dx, dy = 0, -1
        elif key in ['d', 'right']:
            dx, dy = 0, 1
        else:
            return
            
        self.move_player(dx, dy)
    
    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Handle wrapping
        if new_x < 0:
            new_x = self.board.n - 1
        elif new_x == self.board.n:
            new_x = 0
            
        if new_y < 0:
            new_y = self.board.n - 1
        elif new_y == self.board.n:
            new_y = 0
        
        new_pos = (new_x, new_y)
        
        # Check if move is blocked by wall
        if not self.board.has_wall(self.player_pos, new_pos):
            # Move is not blocked
            self.execute_move(new_pos)
        elif self.player.has_jump():
            # Move is blocked but player can jump
            self.show_message("Jumped over wall!", "info")
            self.player.dec_jump()
            self.execute_move(new_pos)
        else:
            # Move is blocked and no jumps available
            self.show_message("Blocked by a wall!", "warning")
    
    def execute_move(self, new_pos):
        # Move player
        self.player.move(new_pos[0], new_pos[1])
        self.player_pos = self.player.get_pos()
        
        # Check for special tiles
        current_tile = self.board.grid[self.player_pos[0]][self.player_pos[1]]
        
        if current_tile == TileColor.ORANGE:
            self.show_message("Acquired a jump token!", "success")
            self.player.inc_jump()
            self.board.clear_square(self.player_pos[0], self.player_pos[1])
        elif current_tile == TileColor.GREEN:
            self.show_victory()
            return
        
        # Update display
        self.update_stats()
        self.draw_board()
    
    def update_stats(self):
        self.stats_label.config(
            text=f"Board: {self.board.n}x{self.board.n} | Jumps: {self.player.jump_tokens} | Position: {self.player_pos}"
        )
    
    def show_message(self, message, msg_type="info"):
        # Show temporary message
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
            
        colors = {
            "info": "#3498DB",
            "success": "#27AE60", 
            "warning": "#E67E22",
            "error": "#E74C3C"
        }
        
        self.message_label = tk.Label(
            self.root,
            text=message,
            bg=colors.get(msg_type, "#3498DB"),
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        self.message_label.pack()
        
        # Remove message after 2 seconds
        self.root.after(2000, lambda: self.message_label.destroy() if hasattr(self, 'message_label') else None)
    
    def show_victory(self):
        messagebox.showinfo("Congratulations!", "🎉 You found the treasure! 🎉\n\nWell played!")
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

def start_gui_game(board_size, num_jumps, density_walls):
    """Start the GUI version of the maze game."""
    game = MazeGameGUI(board_size, num_jumps, density_walls)
    game.run()