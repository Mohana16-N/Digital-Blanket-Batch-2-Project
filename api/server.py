from flask import Flask, request, jsonify
from stable_baselines3 import PPO
import numpy as np

app = Flask(__name__)
model = PPO.load("model/energy_optimizer")

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    state = np.array([
    (data["room_temp"] - 15) / 15,  # Normalize between 0 and 1
    data["outside_temp"] / 50,
    data["energy"] / 100
], dtype=np.float32)

    action, _ = model.predict(state)
    return jsonify({"action": int(action)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

#  Updating server.py to Fetch Real-Time Data
# Now, modify server.py to always fetch real-time data before predicting.

# 🔹 Modify server.py:

# from flask import Flask, request, jsonify
# from stable_baselines3 import PPO
# import numpy as np
# import requests

# app = Flask(__name__)

# # Load trained model
# model = PPO.load("model/energy_optimizer.zip")

# # API endpoint for real-time sensor data
# SENSOR_API_URL = "http://127.0.0.1:5000/sensor-data"

# def get_real_time_sensor_data():
#     """Fetch live data from sensor API before predicting."""
#     try:
#         response = requests.get(SENSOR_API_URL)
#         if response.status_code == 200:
#             return response.json()  # Example response: {"room_temp": 24, "outside_temp": 30, "energy": 40}
#     except:
#         print("Error fetching real-time data. Using default values.")
#     return {"room_temp": 22, "outside_temp": 25, "energy": 50}  # Default fallback values

# @app.route('/optimize', methods=['GET'])
# def optimize():
#     """Fetch real-time sensor data and predict the best action."""
#     data = get_real_time_sensor_data()
#     state = np.array([data["room_temp"], data["outside_temp"], data["energy"]], dtype=np.float32)
    
#     # Predict the best action using the RL model
#     action, _ = model.predict(state)

#     return jsonify({"action": int(action)})

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000)

# ✅ Now, whenever /optimize is called, it will fetch live sensor data instead of requiring manual input!