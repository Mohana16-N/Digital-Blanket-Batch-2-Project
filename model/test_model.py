import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stable_baselines3 import PPO
from env.energy_env import EnergyOptimizationEnv

# Load trained model
model = PPO.load("model/energy_optimizer")

# Create environment
env = EnergyOptimizationEnv()
state, _ = env.reset()

# Run for 10 steps
for _ in range(10):
    action, _ = model.predict(state)
    state, reward, terminated, truncated, _ = env.step(action)
    print(f"Action: {action}, New State: {state}, Reward: {reward}")

    if terminated or truncated:
        break
