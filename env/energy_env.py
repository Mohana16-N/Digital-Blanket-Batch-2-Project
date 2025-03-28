import numpy as np
import gymnasium as gym
from gymnasium import spaces

class EnergyOptimizationEnv(gym.Env):
    def __init__(self):
        super(EnergyOptimizationEnv, self).__init__()

        # Observation space: Room Temp, Outside Temp, Energy Usage
        self.observation_space = spaces.Box(low=np.array([15, 0, 0]), 
                                            high=np.array([30, 50, 100]), 
                                            dtype=np.float32)

        # Action space: 0 (Increase AC), 1 (Decrease AC), 2 (Maintain)
        self.action_space = spaces.Discrete(3)

        # Initial state
        self.state = np.array([22, 25, 50], dtype=np.float32)

    def seed(self, seed=None):
        np.random.seed(seed)

    def step(self, action):
        room_temp, outside_temp, energy = self.state

        # Apply action effect
        if action == 0:  # Increase AC power (cooling)
            room_temp -= 1
            energy += 5
        elif action == 1:  # Decrease AC power (heating)
            room_temp += 1
            energy -= 5

        # Reward function: Encourage 22-24°C, minimize energy, and encourage balance
        reward = -abs(room_temp - 23) - (energy / 50)  

        # Additional reward for efficiency
        if 22 <= room_temp <= 24:
            reward += 5  # Reward for maintaining comfortable temperature
        if action == 1 and energy < 40:
            reward += 3  # Reward for reducing energy when it's too high
        elif action == 0 and energy > 60:
            reward -= 3  # Penalize increasing AC if energy usage is already high

        # No termination condition in this environment
        terminated = False
        truncated = False  # No early stopping

        # Update state
        self.state = np.array([room_temp, outside_temp, energy], dtype=np.float32)

        return self.state, reward, terminated, truncated, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Call parent class reset
        self.state = np.array([22, 25, 50], dtype=np.float32)
        return self.state, {}

'''import numpy as np
import gymnasium as gym
from gymnasium import spaces

class EnergyOptimizationEnv(gym.Env):
    def __init__(self):
        super(EnergyOptimizationEnv, self).__init__()

        # Observation space: Room Temp, Outside Temp, Energy Usage
        self.observation_space = spaces.Box(low=np.array([15, 0, 0]), high=np.array([30, 50, 100]), dtype=np.float32)

        # Action space: 0 (Increase AC), 1 (Decrease AC), 2 (Maintain)
        self.action_space = spaces.Discrete(3)

        # Initial state
        self.state = np.array([22, 25, 50], dtype=np.float32)

    def seed(self, seed=None):
        np.random.seed(seed)

    def step(self, action):
        room_temp, outside_temp, energy = self.state

        # Apply action effect
        if action == 0:  # Increase AC power
            room_temp -= 1
            energy += 5
        elif action == 1:  # Decrease AC power
            room_temp += 1
            energy -= 5

        # Reward function: Encourage comfortable temperatures (22-24°C), minimize energy
        # reward = -abs(room_temp - 23) - (energy / 50) + (5 if action == 1 else 0)  # Reward for increasing efficiency
        reward = -abs(room_temp - 23) - (energy / 50)  




        # No termination condition in this environment
        terminated = False
        truncated = False  # No early stopping

        # Update state
        self.state = np.array([room_temp, outside_temp, energy], dtype=np.float32)

        return self.state, reward, terminated, truncated, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Call parent class reset
        self.state = np.array([22, 25, 50], dtype=np.float32)
        return self.state, {}


'''
# Instead of using a fixed state, fetch data dynamically from another API that provides real-time sensor values.

# 🔹 Modify energy_env.py:

# import requests
# import gymnasium as gym
# from gymnasium import spaces
# import numpy as np

# # API endpoint for fetching real-time sensor data
# API_URL = "http://127.0.0.1:5000/sensor-data"

# def get_real_time_data():
#     """Fetch real-time sensor data from an external API."""
#     try:
#         response = requests.get(API_URL)
#         if response.status_code == 200:
#             return response.json()  # Example response: {"room_temp": 24, "outside_temp": 30, "energy": 40}
#     except:
#         print("Error fetching real-time data. Using default values.")
#     return {"room_temp": 22, "outside_temp": 25, "energy": 50}  # Default values

# class EnergyOptimizationEnv(gym.Env):
#     def __init__(self):
#         super(EnergyOptimizationEnv, self).__init__()

#         self.observation_space = spaces.Box(low=np.array([15, 0, 0]), high=np.array([30, 50, 100]), dtype=np.float32)
#         self.action_space = spaces.Discrete(3)

#         # Get real-time sensor data instead of using a fixed state
#         data = get_real_time_data()
#         self.state = np.array([data["room_temp"], data["outside_temp"], data["energy"]], dtype=np.float32)
