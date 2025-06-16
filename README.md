# 🧠 Maze Runner RL

A Python-based grid-world environment for learning and experimenting with reinforcement learning (RL), featuring both GUI and terminal modes. You, the player, must navigate from start to finish, collect jump tokens, and avoid walls — or jump over them like a caffeinated ninja.

## 🎯 Project Purpose

This project is designed as a foundational learning environment to understand how agents interact with environments — a DIY OpenAI Gym-style simulation. It’s great for:

- Understanding environment-agent loops  
- Practicing RL algorithm development  
- Exploring game mechanics like rewards, obstacles, and power-ups  
- Having way too much fun for a grid-based game  

## 🕹️ Features

- ✅ Terminal and GUI game modes  
- ✅ Wraparound grid (because edges are for rookies)  
- ✅ Procedural wall generation with adjustable density  
- ✅ Jump tokens that allow you to vault over walls  
- ✅ Orange tiles = free jumps! 🍊  
- ✅ Green tile = treasure! 🎉  

## 🚀 Getting Started

### Requirements

- Python 3.8+
- Standard libraries (if your `mazegui.py` has dependencies like `pygame`, list them below)
- Local modules:
  - `board.py`
  - `player.py`
  - `mazegui.py`

### Running the Game

```bash
python main.py -n 8 -j 3 -d 0.3 -t 0
````

| Flag | Description                     |
| ---- | ------------------------------- |
| `-n` | Size of the board (must be ≥ 5) |
| `-j` | Number of jump tokens           |
| `-d` | Density of walls (0 < d < 1)    |
| `-t` | Mode: `1` = Terminal, `0` = GUI |

Example:

```bash
python main.py -n 10 -j 2 -d 0.2 -t 1
```

## 🎮 Controls (Terminal Mode)

Use **WASD** keys to move:

* `w` - move up
* `a` - move left
* `s` - move down
* `d` - move right
* `h` - show help
* `q` - quit the game

### Game Rules

* Walls may block your movement.
* If you have jump tokens, you can jump over a wall.
* Orange tiles (`ORANGE`) give you jump tokens.
* Reach the green tile (`GREEN`) to win!

## 📁 Project Structure

```
├── main.py         # CLI & game loop entry
├── board.py        # Board logic & tile definitions
├── player.py       # Player state & movement
└── mazegui.py      # GUI game mode (optional)
```

## 🤖 Future Plans

* Implement reinforcement learning agents (Q-Learning, DQN)
* Wrap the game as a custom `gym.Env` environment
* Add logging, analytics, and replay capabilities
* Introduce enemy bots or dynamic hazards

## 📚 Learning Outcome

This project helped me:

* Design agent-environment loops like in OpenAI Gym
* Create a modular game structure
* Implement basic game logic like walls, power-ups, and goals
* Laugh maniacally while debugging recursive wall placement

## 🪪 License

MIT — free as your jumps after finding an orange square 🍊

