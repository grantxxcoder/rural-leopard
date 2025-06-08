from environment import MazeWorldEnv
from stable_baselines3 import PPO


def main():
    print(f"Start model process")
    # Simple training
    env = MazeWorldEnv(min_size=8, max_size=8)
    model = PPO("MultiInputPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save("quick_test_model")
    
    # Quick test
    obs, _ = env.reset()
    for _ in range(50):
        action, _ = model.predict(obs)
        obs, reward, done, truncated, info = env.step(action)
        if done:
            print("Agent reached the goal!")
            break

def watch_agent_play(model_path, show_board=True):
    model = PPO.load(model_path)
    env = MazeWorldEnv(min_size=8, max_size=8)
    
    obs, _ = env.reset()
    done = False
    step = 0
    
    if show_board:
        print("Initial board:")
        env.board.print_grid(tuple(obs['agent']))
    
    while not done and step < 50:
        action, _ = model.predict(obs, deterministic=True)
        print(f"Action to take: {action}")
        obs, reward, done, truncated, info = env.step(action)
        step += 1
        
        action_names = ['RIGHT', 'UP', 'LEFT', 'DOWN']
        print(f"\nStep {step}: {action_names[action]} -> Reward: {reward}")
        
        if show_board:
            env.board.print_grid(tuple(obs['agent']))
        
        if done:
            print(f"🎉 Agent won in {step} steps!")

# Run it
watch_agent_play("quick_test_model")

# if __name__ == "__main__":
#     main()