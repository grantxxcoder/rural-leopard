import gymnasium as gym
import numpy as np
from board import Board, TileColor
from player import Player
import random

class MazeWorldEnv(gym.Env):
    def __init__(self, min_size=8, max_size=15):
        self.min_size = min_size
        self.max_size = max_size
        self.current_size = min_size
        
        self.max_steps = 200  # Prevent infinite episodes
        self.step_count = 0


        # create the components
        self.board = None
        self.player = None

        # Define the agent and target location; randomly chosen in `reset` and updated in `step`
        self._agent_location = np.array([-1, -1], dtype=np.int32)
        self._target_location = np.array([-1, -1], dtype=np.int32)

        self.observation_space = gym.spaces.Dict({
            "agent": gym.spaces.Box(0, max_size - 1, shape=(2,), dtype=int),
            "target": gym.spaces.Box(0, max_size - 1, shape=(2,), dtype=int),
            "board_size": gym.spaces.Box(min_size, max_size, shape=(1,), dtype=int),
            "jumps_remaining": gym.spaces.Box(0, 3, shape=(1,), dtype=int),
            # Optional: include board state
            "walls": gym.spaces.Box(0, 1, shape=(max_size, max_size, 4), dtype=int)  # 4 directions
        })

        # We have 4 actions, corresponding to "right", "up", "left", "down"
        self.action_space = gym.spaces.Discrete(4)
        # Dictionary maps the abstract actions to the directions on the grid
        self._action_to_direction = {
            0: np.array([1, 0]),  # right
            1: np.array([0, 1]),  # up
            2: np.array([-1, 0]),  # left
            3: np.array([0, -1]),  # down
        }
    
    def reset(self, seed=None, options=None):
        # Handle seeding for reproducibility
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.step_count = 0
        num_jumps = random.randint(0, 3)
        density_walls = random.uniform(0.5, 0.8)

        # Create new board each episode
        self.board = Board(self.current_size, num_jumps, density_walls)
        self.player = Player()
        
        # Get positions from your board
        self._agent_location = np.array(self.player.get_pos())
        self._target_location = np.array(self.board.get_treasure_pos())  # You'll need this method
        return self._get_obs(), {}

    def _calculate_new_position(self, pos, direction):
        dx = direction[0]
        dy = direction[1]

        new_x = pos[0] + dx
        new_y = pos[1] + dy

        # Handle wrapping
        if (new_x < 0):
            new_x = self.current_size - 1
        elif new_x == self.current_size:
            new_x = 0
        
        if (new_y < 0):
            new_y = self.current_size - 1
        elif (new_y == self.current_size):
            new_y = 0

        new_pos = (new_x, new_y)
        return new_pos

    def step(self, action):
        self.step_count += 1
    
        direction = self._action_to_direction[int(action)]
        current_pos = tuple(self._agent_location)
        
        # Calculate new position with wrapping
        new_pos = self._calculate_new_position(current_pos, direction)
        
        # Check if move is valid using your existing board logic
        if not self.board.has_wall(current_pos, new_pos):
            # Valid move
            self._agent_location = np.array(new_pos)
            self.player.move(new_pos[0], new_pos[1])
            reward = -1  # Step penalty
            
        elif self.player.has_jump():
            # Invalid move but can jump
            self._agent_location = np.array(new_pos)
            self.player.move(new_pos[0], new_pos[1])
            self.player.dec_jump()
            reward = -1  # Step penalty
            
        else:
            # Invalid move, can't jump - agent stays in place
            reward = -1  # Still penalize the attempted move
        
        # Check for special tiles, goal, etc.
        # Check win condition
        done = False
        current_pos = tuple(self._agent_location)
        if self.board.grid[current_pos[0]][current_pos[1]] == TileColor.GREEN:
            reward += 100  # Big reward for winning
            done = True

        # reward collecting a jump
        if self.board.grid[current_pos[0]][current_pos[1]] == TileColor.ORANGE:
            self.player.inc_jump()
            self.board.clear_square(current_pos[0], current_pos[1])
            reward += 5

        if self.step_count >= self.max_steps:
            done = True
            reward -= 10  # Small penalty for timeout

        obs = self._get_obs()
        info = {"step_count": self.step_count}
           
        return obs, reward, done, False, info  # (obs, reward, terminated, truncated, info)
    
    def _get_obs(self):
        return {
            "agent": self._agent_location,
            "target": self._target_location, 
            "board_size": np.array([self.current_size]),
            "jumps_remaining": np.array([self.player.get_jumps()]),
            "walls": self._get_wall_representation()
        }
    
    def _check_if_done(self):
        current_pos = tuple(self._agent_location)
        return self.board.grid[current_pos[0]][current_pos[1]] == TileColor.GREEN
    
    def _get_wall_representation(self):
        walls = np.zeros((self.max_size, self.max_size, 4), dtype=int)
        
        # Direct access to wall set - much faster!
        for wall in self.board.walls:
            wall_type, row, col = wall
            
            if wall_type == 'h':  # Horizontal wall blocks up/down movement
                # Horizontal wall below (row, col) blocks downward movement FROM (row, col)
                if row < self.current_size and col < self.current_size:
                    walls[row, col, 3] = 1  # Block DOWN from (row, col)
                # And blocks upward movement TO (row, col) from (row+1, col)
                if row + 1 < self.current_size and col < self.current_size:
                    walls[row + 1, col, 1] = 1  # Block UP from (row+1, col)
                    
            elif wall_type == 'v':  # Vertical wall blocks left/right movement
                # Vertical wall to right of (row, col) blocks rightward movement FROM (row, col)
                if row < self.current_size and col < self.current_size:
                    walls[row, col, 0] = 1  # Block RIGHT from (row, col)
                # And blocks leftward movement TO (row, col) from (row, col+1)
                if row < self.current_size and col + 1 < self.current_size:
                    walls[row, col + 1, 2] = 1  # Block LEFT from (row, col+1)
        
        return walls