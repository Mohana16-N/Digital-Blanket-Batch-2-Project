import sys
sys.path.append("./")  # Ensure Python finds the module

import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from env.energy_env import EnergyOptimizationEnv

# Create vectorized environment
env = make_vec_env(EnergyOptimizationEnv, n_envs=1)

# Initialize PPO model
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
# model.learn(total_timesteps=10000)
model.learn(total_timesteps=100000)  # Train for a longer period
 # Increase training time


# Save the trained model
model.save("model/energy_optimizer")
print("Model training complete and saved as 'model/energy_optimizer.zip'")


