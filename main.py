from blackjackagent import BlackjackAgent
from tqdm import tqdm
import gymnasium as gym
from matplotlib import pyplot as plt
import numpy as np

def get_moving_avgs(arr, window, convolution_mode):
    return np.convolve(
        np.array(arr).flatten(),
        np.ones(window),
        mode=convolution_mode
    ) / window

def plot(env, agent):
    # Smooth over a 500 episode window
    rolling_length = 500
    fig, axs = plt.subplots(ncols=3, figsize=(12, 5))

    axs[0].set_title("Episode rewards")
    reward_moving_average = get_moving_avgs(
        env.return_queue,
        rolling_length,
        "valid"
    )
    axs[0].plot(range(len(reward_moving_average)), reward_moving_average)

    axs[1].set_title("Episode lengths")
    length_moving_average = get_moving_avgs(
        env.length_queue,
        rolling_length,
        "valid"
    )
    axs[1].plot(range(len(length_moving_average)), length_moving_average)

    axs[2].set_title("Training Error")
    training_error_moving_average = get_moving_avgs(
        agent.training_error,
        rolling_length,
        "same"
    )
    axs[2].plot(range(len(training_error_moving_average)), training_error_moving_average)
    plt.tight_layout()
    plt.show()

def train():
    learning_rate = 0.01
    n_episodes = 10_000_000
    start_epsilon = 1.0
    epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
    final_epsilon = 0.1
    env = gym.make("Blackjack-v1", sab=False)
    env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)

    agent = BlackjackAgent(
        env=env,
        learning_rate=learning_rate,
        initial_epsilon=start_epsilon,
        epsilon_decay=epsilon_decay,
        final_epsilon=final_epsilon,
    )

    for episode in tqdm(range(n_episodes)):
        obs, info = env.reset()
        done = False

        # play one episode
        while not done:
            action = agent.get_action(obs)
            next_obs, reward, terminated, truncated, info = env.step(action)

            # update the agent
            agent.update(obs, action, reward, terminated, next_obs)

            # update if the environment is done and the current obs
            done = terminated or truncated
            obs = next_obs

        agent.decay_epsilon()
    
    plot(env=env, agent=agent)
    return env, agent

def test(env, agent):
    print("\nTesting the agent...")
    agent.epsilon = 0  # No more random actions, only use learned strategy

    wins = 0
    games = 1000

    for game in range(games):
        obs, info = env.reset()
        done = False
        
        while not done:
            action = agent.get_action(obs)  # Use learned strategy
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
        
        if reward > 0:  # Win
            wins += 1

    win_rate = wins / games
    print(f"Win rate: {win_rate:.1%} ({wins}/{games} games)")

    # 5. EXAMPLE: See what the agent learned
    print("\nExample of learned strategy:")
    print("State (player_sum, dealer_card, usable_ace) -> Action (0=stand, 1=hit)\n")

    # Show some example states and what the agent learned
    example_states = [
        (20, 10, False),  # Player has 20, dealer shows 10
        (12, 6, False),   # Player has 12, dealer shows 6  
        (16, 10, False),  # Player has 16, dealer shows 10
        (11, 9, False),   # Player has 11, dealer shows 9
    ]

    for state in example_states:
        if state in agent.q_values:
            action = np.argmax(agent.q_values[state])
            action_name = "Stand" if action == 0 else "Hit"
            q_vals = agent.q_values[state]
            print(f"{state} -> {action_name} (Q-values: Stand={q_vals[0]:.2f}, Hit={q_vals[1]:.2f})")
            
def main():
    print("Start")
    env, agent = train()
    test(env=env, agent=agent)
    
    

if __name__ == "__main__":
    main()
