# 🦁 Rural Leopard: Treasure Hunt

A DIY OpenAI Gym–style grid‐world where you guide your “leopard” (player) through a wraparound maze full of walls, jump tokens, and—and ultimately—a glittering green treasure tile. Choose between a terminal or GUI interface, collect orange tokens to vault over walls, and prove you’re the king of the savanna.

## 🚀 Quick Start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/grantxxcoder/rural-leopard.git
   cd rural-leopard/treasurehunt
   ```

2. **Install dependencies**

   * Core: Python 3.8+
   * GUI mode (if you plan to use it):

     ```bash
     pip install pygame
     ```

3. **Run the game**

   ```bash
   python main.py -n 10 -j 3 -d 0.25 -t 0
   ```

   Flags:

   * `-n` (int ≥ 5): board size
   * `-j` (int ≥ 0): initial jump tokens
   * `-d` (0 < float < 1): wall density
   * `-t` (0 or 1): mode 0 = GUI, 1 = Terminal

## 🎮 Terminal Controls

* **w** – up
* **a** – left
* **s** – down
* **d** – right
* **h** – help
* **q** – quit

🏃 Move around; walls block you unless you spend a jump token (orange tiles give +1 jump). Reach the green tile to win! 🎉

## 🗂️ Project Layout

```
treasurehunt/
├── main.py         # CLI argument parsing & mode selector
├── board.py        # Maze and tile logic  
├── player.py       # Player state, position, jump tokens  
└── mazegui.py      # Optional Pygame GUI mode  
```

## 🤖 Reinforcement‑Learning Hook

This environment is ripe for wrapping in a custom `gym.Env`:

* Define `step()`, `reset()`, `render()`
* Add a reward scheme (e.g. +100 for treasure, –1 per move)
* Plug in Q‑learning, SARSA, or DQN agents

## 🛠️ Future Ideas

* 🎯 A Gym wrapper (`pip install rural-leopard`)
* 📊 Logging & training curve plotting
* 🤼‍♀️ AI “leopard vs. leopard” duels
* 🦁 Wild beasts (moving obstacles)

```
